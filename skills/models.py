from django.db import models
from django.contrib.auth.models import User


class SkillPost(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'Technology & Coding'),
        ('academic', 'Academic Tutoring'),
        ('language', 'Language & Writing'),
        ('music', 'Music & Arts'),
        ('design', 'Design & Media'),
        ('fitness', 'Fitness & Wellness'),
        ('cooking', 'Cooking & Food'),
        ('other', 'Other'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skill_posts')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    rate = models.CharField(max_length=100, help_text="e.g. Free, $15/hr, Trade for coffee")
    contact = models.CharField(max_length=200, help_text="How students should reach you")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.author.username}"

    def get_category_display_label(self):
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)


class Appointment(models.Model):
    skill_post = models.ForeignKey(SkillPost, on_delete=models.CASCADE, related_name='appointments')
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField(blank=True, help_text="Optional note for the skill provider")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.requester.username} → {self.skill_post.title} on {self.date} at {self.time}"


class Review(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]

    skill_post = models.ForeignKey(SkillPost, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('skill_post', 'reviewer')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reviewer.username} rated '{self.skill_post.title}': {self.rating}/5"
