def create_module(app, **kwargs):
    from .controllers import qa_blueprint
    app.register_blueprint(qa_blueprint)
