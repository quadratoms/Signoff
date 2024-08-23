from django.urls import path
from .views import (
    ApprovalDetailView,
    ApprovalListCreateView,
    FormTypeListCreateView,
    FormTypeRetrieveUpdateDestroyView,
    DynamicFormFieldListCreateView,
    DynamicFormFieldRetrieveUpdateDestroyView,
    DynamicFormFieldValueListCreateView,
    DynamicFormFieldValueRetrieveUpdateDestroyView,
    SignInView,
    SignUpView,
    UserRequestDetailView,
    UserRequestListCreateView,
    UserListView
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

...

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signin/", SignInView.as_view(), name="signin"),
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # FormType URLs
    path("users/", UserListView.as_view(), name="user-list"),
    path("formtypes/", FormTypeListCreateView.as_view(), name="formtype-list"),
    path(
        "formtypes/<int:pk>/",
        FormTypeRetrieveUpdateDestroyView.as_view(),
        name="formtype-detail",
    ),
    # DynamicFormField URLs
    path(
        "dynamicformfields/",
        DynamicFormFieldListCreateView.as_view(),
        name="dynamicformfield-list",
    ),
    path(
        "dynamicformfields/<int:pk>/",
        DynamicFormFieldRetrieveUpdateDestroyView.as_view(),
        name="dynamicformfield-detail",
    ),
    # DynamicFormFieldValue URLs
    path(
        "dynamicformfieldvalues/",
        DynamicFormFieldValueListCreateView.as_view(),
        name="dynamicformfieldvalue-list",
    ),
    path(
        "dynamicformfieldvalues/<int:pk>/",
        DynamicFormFieldValueRetrieveUpdateDestroyView.as_view(),
        name="dynamicformfieldvalue-detail",
    ),
    # UserRequest URLs
    path("userrequests/", UserRequestListCreateView.as_view(), name="userrequest-list"),
    path(
        "userrequests/<int:pk>/",
        UserRequestDetailView.as_view(),
        name="userrequest-detail",
    ),
    path("approvals/", ApprovalListCreateView.as_view(), name="approval-list-create"),
    path("approvals/<int:pk>/", ApprovalDetailView.as_view(), name="approval-detail"),
]
