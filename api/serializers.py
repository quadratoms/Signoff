from rest_framework import serializers

from client_app.models import (
    Approval,
    DynamicFormField,
    DynamicFormFieldValue,
    FormType,
    UserRequest,
)

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "email")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class DynamicFormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = DynamicFormField
        fields = [field.name for field in model._meta.fields]
        # fields.remove("form_type")


class FormTypeSerializer(serializers.ModelSerializer):
    dynamic_form_type = DynamicFormFieldSerializer(many=True, required=False)

    class Meta:
        model = FormType
        fields = [field.name for field in model._meta.fields]
        fields.append("dynamic_form_type")

    def create(self, validated_data):
        dynamicFormFields = validated_data.pop("dynamic_form_type", [])
        form_type = FormType.objects.create(**validated_data)

        for dynamic_data in dynamicFormFields:
            dy, _ = DynamicFormField.objects.get_or_create(**dynamic_data)

            form_type.dynamic_form_type.add(dy)
            # dy,_ = DynamicFormField.objects.get_or_create(**dynamic_data)
            # dy.form_type.add(form_type)

        return form_type
    
    def update(self, instance, validated_data):
        dynamicFormFields = validated_data.pop("dynamic_form_type", [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        for dynamic_data in dynamicFormFields:
            dy, _ = DynamicFormField.objects.get_or_create(**dynamic_data)

            instance.dynamic_form_type.add(dy)

        
        return super().update(instance, validated_data)


class DynamicFormFieldValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = DynamicFormFieldValue
        fields = "__all__"


class UserRequestSerializer(serializers.ModelSerializer):
    """_summary_

    For list and view
    """

    user_request_form_v = DynamicFormFieldValueSerializer(many=True, read_only=True)
    dynamic_fields = serializers.DictField(write_only=True, required=False)

    class Meta:
        model = UserRequest
        fields = [field.name for field in model._meta.fields]
        # fields.append("representation")
        fields.append("user_request_form_v")
        fields.append("dynamic_fields")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        form_fields = DynamicFormField.objects.filter(form_type=instance.form_type)
        print(form_fields)
        # for field in form_fields:
        #     field_label = field.label
        #     # if field_label in representation:
        #     value_instance = DynamicFormFieldValue.objects.filter(user_request=instance, label=field)
        #     if value_instance.exists():
        #         representation[field_label] = value_instance.first().field_value
        # # print(representation)
        return representation


class ApprovalSerializer(serializers.ModelSerializer):
    users= UserSerializer()
    class Meta:
        model = Approval
        fields = "__all__"


class UserRequestWithApprovalsSerializer(serializers.ModelSerializer):
    user_request_approvals = ApprovalSerializer(many=True, required=False)
    created_by = UserSerializer(required=False)
    user_request_form_v = DynamicFormFieldValueSerializer(many=True, read_only=True)
    dynamic_fields = serializers.DictField(write_only=True, required=False)

    class Meta:
        model = UserRequest
        fields = [field.name for field in model._meta.fields]

        fields.append("user_request_form_v")
        fields.append("dynamic_fields")  # not need
        fields.append("user_request_approvals")
        fields.append("created_by")

    def create(self, validated_data: dict):
        approvals_data = validated_data.pop("user_request_approvals", [])
        dynamic_fields: dict = validated_data.pop("dynamic_fields", {})
        user_request = UserRequest.objects.create(**validated_data)
        validated_data['creaated_by'] = self.context['request'].user
        if len(approvals_data)==0:
            raise ValueError


        allowed_fields = [c.label for c in user_request.form_type.dynamic_form_type.all()]
        print(allowed_fields)

        for each in allowed_fields:
            if each in dynamic_fields.keys():
                d, _ = DynamicFormFieldValue.objects.get_or_create(
                    label=each,
                    user_request=user_request
                )
                d.field_value=dynamic_fields[each]
                d.save()
                # instance.user_request_form_v.add(d)

        b = user_request.user_request_form_v.all()

        for approval_data in approvals_data:
            Approval.objects.create(user_request=user_request, **approval_data)

        return user_request

    def update(self, instance, validated_data):
        dynamic_fields: dict = validated_data.pop("dynamic_fields", {})
        approvals_data = validated_data.pop("user_request_approvals", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        allowed_fields = [c.label for c in instance.form_type.dynamic_form_type.all()]
        print(allowed_fields)

        for each in allowed_fields:
            if each in dynamic_fields.keys():
                d, _ = DynamicFormFieldValue.objects.get_or_create(
                    label=each,
                    user_request=instance
                )
                a=str(dynamic_fields.get(each))
                d.field_value=a
                d.save()
                
        
        # for approval_data in approvals_data:
        #     Approval.objects.get_or_create(request=instance, **approval_data)

        return instance
