from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

class Task(models.Model):
    LOW = 'low'
    MED = 'medium'
    HIGH = 'high'
    PRIORITY_CHOICES = [(LOW,'Low'), (MED,'Medium'), (HIGH,'High')]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=MED)
    # Progress percentage from 0 to 100. Keep in sync with `completed` flag.
    progress = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def clean(self):
        """Model validation: prevent due_date in the past."""
        if self.due_date:
            today = timezone.localdate()
            if self.due_date < today:
                raise ValidationError({'due_date': 'Due date cannot be in the past.'})

    def recompute_progress_from_steps(self):
        """If this task has steps, set progress to percentage of steps completed.

        Returns the new progress integer.
        """
        steps = self.steps.all()
        if not steps:
            return self.progress
        total = steps.count()
        done = steps.filter(done=True).count()
        pct = int((done / total) * 100) if total else 0
        self.progress = pct
        self.completed = (pct >= 100)
        self.save(update_fields=['progress', 'completed'])
        return self.progress


class Step(models.Model):
    task = models.ForeignKey(Task, related_name='steps', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({'done' if self.done else 'pending'})"