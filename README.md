# endi-s_project
With trackback:
Traceback (most recent call last):
      File "/home/realdobeja/.local/lib/python3.8/site-packages/flask/app.py", line 2031, in __call__
        return self.wsgi_app(environ, start_response)
      File "/home/realdobeja/.local/lib/python3.8/site-packages/flask/app.py", line 2017, in wsgi_app
        response = self.handle_exception(e)
      File "/home/realdobeja/.local/lib/python3.8/site-packages/flask/app.py", line 2014, in wsgi_app
        response = self.full_dispatch_request()
      File "/home/realdobeja/.local/lib/python3.8/site-packages/flask/app.py", line 1529, in full_dispatch_request
        rv = self.handle_user_exception(e)
      File "/home/realdobeja/.local/lib/python3.8/site-packages/flask/app.py", line 1527, in full_dispatch_request
        rv = self.dispatch_request()
      File "/home/realdobeja/.local/lib/python3.8/site-packages/flask/app.py", line 1513, in dispatch_request
        return self.view_functions[rule.endpoint](**req.view_args)
      File "/home/realdobeja/Documents/endi's_project/app.py", line 73, in home
        replies = Comment.query.filter_by(author_comment=current_user).order_by(Comment.timestamp.desc()).all()
      File "/home/realdobeja/.local/lib/python3.8/site-packages/sqlalchemy/orm/query.py", line 1921, in filter_by
        clauses = [
      File "/home/realdobeja/.local/lib/python3.8/site-packages/sqlalchemy/orm/query.py", line 1922, in <listcomp>
        _entity_descriptor(zero, key) == value
      File "/home/realdobeja/.local/lib/python3.8/site-packages/sqlalchemy/sql/operators.py", line 365, in __eq__
        return self.operate(eq, other)
      File "/home/realdobeja/.local/lib/python3.8/site-packages/sqlalchemy/orm/attributes.py", line 219, in operate
        return op(self.comparator, *other, **kwargs)
      File "/home/realdobeja/.local/lib/python3.8/site-packages/sqlalchemy/orm/relationships.py", line 1267, in __eq__
        self.property._optimized_compare(
      File "/home/realdobeja/.local/lib/python3.8/site-packages/sqlalchemy/orm/relationships.py", line 1648, in _optimized_compare
        raise sa_exc.ArgumentError(
    sqlalchemy.exc.ArgumentError: Mapped instance expected for relationship comparison to object.   Classes, queries and other SQL elements are not accepted in this context; for comparison with a subquery, use Comment.author_comment.has(**criteria).
