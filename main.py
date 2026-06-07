import sys
from classmods import ENVMod
from devixa_server import (
    cnf,
    db,
    blueprints,
    apps_bp,
    create_app,
    add_error_handler,
    register_extentions,
    register_bluprints,
    init_database,
)

def main() -> int:
    ENVMod.load_dotenv(verbose=True)
    cnf.load_config()
    app = create_app(__name__)
    init_database(app, db)
    add_error_handler(app)
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
