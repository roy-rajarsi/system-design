from apps import mobile_app, web_app
from responses import admin_response, customer_response


def main() -> None:

    # Admin user on mobile
    mobile_application: mobile_app.MobileApp = mobile_app.MobileApp(admin_response.AdminResponse(user_id=22))
    print(f"Admin on mobile sees -> {mobile_application.render_ui()}")

    # Customer on web browser
    web_application: web_app.WebApp = web_app.WebApp(customer_response.CustomerResponse(user_id=24))
    print(f"Customer on web browser sees -> {web_application.render_ui()}")


if __name__ == "__main__":
    main()
