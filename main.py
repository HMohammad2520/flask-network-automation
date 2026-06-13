import sys
from classmods import ENVMod
from devixa_server.models import User
from devixa_server import (
    cnf,
    db,
    blueprints,
    apps_bp,
    create_app,
    register_extentions,
    register_bluprints,
    init_database,
    init_user_management,
    init_admin_user,
)

def main() -> int:
    ENVMod.load_dotenv(verbose=True)
    cnf.load_config()
    app = create_app(__name__)
    init_database(app, db)
    init_user_management(app, User)
    init_admin_user(app, User)
    register_extentions(apps_bp)
    register_bluprints(app, blueprints)

    app.run(
        host=cnf.flask_host,
        port=cnf.flask_port,
        debug=cnf.flask_debug,
    )

    return 0


if __name__ == '__main__':
    sys.exit(main())
