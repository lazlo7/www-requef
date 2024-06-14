from fastapi.templating import Jinja2Templates


__templates = Jinja2Templates(directory="www_requef/templates")
def get_templates() -> Jinja2Templates:
    return __templates
