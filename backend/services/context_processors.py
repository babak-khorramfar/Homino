from django.urls import reverse


def nav_items(request):
    if not request.user.is_authenticated:
        return {}

    user_type = getattr(getattr(request.user, "profile", None), "user_type", None)

    if request.user.is_superuser:
        user_type = "superuser"

    if user_type == "customer":
        items = [
            {
                "label": "Home",
                "icon": "fas fa-home",
                "url": reverse("home"),
                "match": "/home/",
            },
            {
                "label": "Services",
                "icon": "fas fa-layer-group",
                "url": reverse("service_list"),
                "match": "/categories/",
            },
            {
                "label": "Requests",
                "icon": "fas fa-list",
                "url": reverse("request_list"),
                "match": "/requests/",
            },
            {
                "label": "Profile",
                "icon": "fas fa-user",
                "url": "#",
                "match": "/profile/",
            },
        ]
    elif user_type == "provider" or user_type == "superuser":
        items = [
            {
                "label": "Offers",
                "icon": "fas fa-briefcase",
                "url": reverse("request_list"),
                "match": "/requests/",
            },
            {
                "label": "My Proposals",
                "icon": "fas fa-paper-plane",
                "url": "#",
                "match": "/proposals/",
            },
            {
                "label": "Support",
                "icon": "fas fa-headset",
                "url": "#",
                "match": "/support/",
            },
            {
                "label": "Logout",
                "icon": "fas fa-sign-out-alt",
                "url": reverse("logout"),
                "match": "/logout/",
            },
        ]
    else:
        items = []

    current_path = request.path
    for item in items:
        item["active"] = item["match"] in current_path

    return {"nav_items": items}
