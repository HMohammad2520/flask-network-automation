import sys
from classmods import ENVMod
from application import (
    cnf,
    blueprints,
    db,
    create_app,
    add_error_handler,
    register_bluprints,
    init_database,
)

def main() -> int:
    ENVMod.load_dotenv()
    app = create_app(__name__)
    init_database(app, db)
    add_error_handler(app)
    register_bluprints(app, blueprints)

    app.run(
        host=cnf.flask_bind,
        port=cnf.flask_port,
        debug=cnf.flask_debug,
    )

    return 0


if __name__ == '__main__':
    sys.exit(main())
