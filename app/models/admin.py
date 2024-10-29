from sqladmin import ModelView

from app.models.order import Order
from app.models.user import User


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.first_name,
        User.last_name,
        User.email,
        User.password,
        User.is_active,
        User.role,
        User.created_at,
        User.updated_at,
    ]


class OrderAdmin(ModelView, model=Order):
    column_list = [
        Order.id,
        Order.product,
        Order.deadline,
        Order.for_final_date,
        Order.language,
        Order.level,
        Order.service,
        Order.quantity,
        Order.space,
        Order.words_count,
        Order.size_type,
        Order.topic,
        Order.description,
        Order.price,
        Order.subject,
        Order.number_of_sources,
        Order.style,
        Order.is_private,
        Order.promocode,
        Order.client_id,
        Order.status,
        Order.created_at,
    ]

    filter_list = [
        Order.id,
        Order.status,
        Order.language,
        Order.level,
        Order.service,
        Order.client_id,
    ]

    search_list = [
        Order.topic,
        Order.description,
        Order.subject,
    ]

    list_display = [
        'id',
        'product',
        'deadline',
        'status',
        'client',
        'created_at',
    ]

    list_filter = [
        'status',
        'language',
        'level',
        'service',
        'client',
    ]

    list_search = [
        'topic',
        'description',
        'subject',
    ]

    form_exclude = [
        'created_at',
    ]

    def client(self, obj):
        return obj.client.first_name + ' ' + obj.client.last_name
    client.short_description = 'Client'