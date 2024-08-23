from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_init, pre_save, post_save
from django.dispatch import receiver


class FormType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


FIELD_TYPE_CHOICES = [
    ("CharField", "CharField"),
    ("ChoiceField", "ChoiceField"),
    ("IntegerField", "IntegerField"),
    ("DateField", "DateField"),
    ("EmailField", "EmailField"),
    ("DecimalField", "DecimalField"),
    ("BooleanField", "BooleanField"),
    ("TextField", "TextField"),
    # Add more choices as needed
]


class DynamicFormField(models.Model):
    form_type = models.ManyToManyField(FormType, related_name="dynamic_form_type")
    label = models.CharField(max_length=255)
    field_type = models.CharField(max_length=50, choices=FIELD_TYPE_CHOICES)
    options= models.CharField(max_length=50, blank=True, null=True)
    is_required = models.BooleanField(default=False)

    def __str__(self):
        return self.label


class Approval(models.Model):
    users = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_approvals"
    )
    request = models.ForeignKey(
        "UserRequest",
        on_delete=models.CASCADE,
        related_name="user_request_approvals",
        blank=True,
        null=True,
    )
    comment = models.TextField(blank=True, null=True)
    signature = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Level {self.request.__str__()}"


class UserRequest(models.Model):
    form_type = models.ForeignKey(FormType, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_by"
    )
    current_approval_level = models.PositiveIntegerField(default=1)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    # def approve(self):
    #     if self.current_approval_level < self.request_approvals.count():
    #         self.current_approval_level += 1
    #     else:
    #         self.completed = True
    #     self.save()

    def reject(self):
        # Handle rejection logic if needed
        pass

    def __init__(self, *args, **kwargs):
        super(UserRequest, self).__init__(*args, **kwargs)

        # Dynamically add fields based on the associated form type
        # if self.form_type:
        #     form_fields = DynamicFormField.objects.filter(form_type=self.form_type)
        #     for field in form_fields:
        #         if field.field_type == "CharField":
        #             setattr(
        #                 self,
        #                 field.label,
        #                 models.CharField(max_length=255, null=True, blank=True),
        #             )
        #         elif field.field_type == "IntegerField":
        #             setattr(
        #                 self, field.label, models.IntegerField(null=True, blank=True)
        #             )
        # Add more field types as needed


@receiver(pre_init, sender=UserRequest)
def kk(sender, instance=None, created=False, **kwargs):
    # d = DynamicFormFieldValue.objects.filter(user_request=instance)
    # for field in d:
    #     setattr(
    #         instance,
    #         field.label,
    #         field.field_value,
    #     )
    pass


@receiver(post_save, sender=UserRequest)
def kkd(sender, instance=None, created=False, **kwargs):
    # allowed_fields = [c.label for c in instance.form_type.dynamic_form_type.all()]
    # print(allowed_fields)
    # a = instance.user_request_form_v.all()
    # # instance.dynamicformfieldvalue_set.filter(label__notin=allowed_fields).delete()
    # print(a)
    # instance.user_request_form_v.exclude(label__label__in=allowed_fields).delete()
    # for each in allowed_fields:
    #     print(dir(instance.dynamic_fields))
    #     if each in instance.dynamic_fields.keys():
    #         d, _ = DynamicFormFieldValue.objects.get_or_create(
    #             user_request=instance,
    #             label__label=each,
    #         )
    #         d.field_value = instance.dynamic_fields[each]
    #         d.save()

    # b = instance.user_request_form_v.all()
    # print(b)
    pass


class DynamicFormFieldValue(models.Model):
    user_request = models.ForeignKey(
        "UserRequest",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="user_request_form_v",
    )
    label = models.CharField(max_length=50)
    field_value = models.CharField(max_length=50)

    def __str__(self):
        return self.label

        """
        When querying related fields, consider using select_related or prefetch_related to optimize database queries and reduce the number of queries executed.

python
Copy code
# Example in views or wherever you are fetching UserRequest instances
queryset = UserRequest.objects.select_related('form_type').prefetch_related('dynamicformfieldvalue_set', 'form_type__dynamicformfield_set')

        """
