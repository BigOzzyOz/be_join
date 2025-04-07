from rest_framework.routers import SimpleRouter
from django.urls import path


class CustomRouter(SimpleRouter):
    extra_routes = []

    def register_extra_route(self, route, view, name):
        self.extra_routes.append(path(route, view.as_view(), name=name))

    def get_urls(self):
        return super().get_urls() + self.extra_routes
