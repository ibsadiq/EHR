from django import template

register = template.Library()


@register.filter
def extract_error_messages(messages):
    error_list = []
    for error_dict in messages:
        print(error_dict)
        for field, error_messages_list in error_dict.items():
            for error_message in error_messages_list:
                error_list.append(
                    {"field": field.capitalize(), "message": error_message}
                )
    return error_list
