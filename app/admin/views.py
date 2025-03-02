from markupsafe import Markup
from sqladmin import ModelView
from sqladmin.fields import Any
from wtforms.fields.simple import TextAreaField

from app.models.actor import Actor
from app.models.movie import Movie, Genre
from app.models.news import News
from app.models.user import User


class UserAdmin(ModelView, model=User, prefix=""):
    # список исключаемых полей из модели
    form_excluded_columns = [User.hashed_password]

    # список отображаемых полей из модели
    column_list = [User.id, User.first_name, User.last_name, User.email,
                   User.gender]

    # список исключаемых полей в отображении на детальном просмотре
    column_details_exclude_list = [User.hashed_password]

    # список полей по которым разрешена сортировка
    column_sortable_list = [User.id, User.first_name, User.last_name,
                            User.email, User.gender]

    # список полей по которым разрешен поиск
    column_searchable_list = [c.name for c in User.__table__.c]

    # поле с сортировкой по умолчанию
    column_default_sort = [(User.id, True)]

    # переименование исходных заголовков столбцов
    column_labels = {User.id: "id", User.email: "Email", User.first_name: "Имя",
                     User.last_name: "Фамилия", User.gender: "Пол",
                     User.created_at: "Дата создания записи",
                     User.country: "Страна",
                     User.is_active: "Активность аккаунта",
                     User.username: "Логин", User.phone: "Телефон",
                     User.avatar: "Аватар",
                     User.updated_at: "Дата обновления записи",
                     User.hashed_password: "Пароль"}

    # разрешение/запрет на действия по удалению
    can_delete = False

    # разрешение/запрет на действия по добавлению
    can_create = False

    # возможность редактировать
    can_edit = True

    # имя таблицы в единственном числе
    name = "пользователь"

    # имя таблицы во множественном числе
    name_plural = "Пользователи"

    # иконка для отображения в меню
    icon = "fa-solid fa-user"


class MovieAdmin(ModelView, model=Movie):
    # Указываем, что поля будут отображаться как TextArea
    form_overrides = {'actors': TextAreaField,
                      'producer': TextAreaField,
                      'screenwriter': TextAreaField,
                      'operator': TextAreaField,
                      'composer': TextAreaField,
                      'editor': TextAreaField}

    async def on_model_change(
            self, data: dict, model: Any, is_created: bool, request
    ) -> None:
        columns = ['producer', 'screenwriter', 'operator', 'composer', 'actors',
                   'editor']
        # Проверяем, есть ли название поля в данных
        for column_name in columns:
            if column_name in data:
                # Получаем строку с именем поля
                column_str = data[column_name]
                # Разделяем строку по запятой и удаляем лишние пробелы
                column_list = [column_name.strip() for column_name in
                               column_str.split(',')]
                # Записываем в модель полученные данные
                data[column_name] = column_list

    def empty_formatter(value: any) -> str:
        """Возвращает '-' для `None` значений"""
        if value:
            return value
        return "-"

    # базовая настройка отображения None,{},[] в Form list
    column_type_formatters = {type(None): empty_formatter,
                              type({}): empty_formatter,
                              type([]): empty_formatter}

    # настройка отображения JSON строк друг под другом в Form list
    column_formatters = {
        Movie.producer: lambda m, a: Markup('<br>'.join(m.producer)),
        Movie.screenwriter: lambda m, a: Markup(
            '<br>'.join(m.screenwriter)),
        Movie.operator: lambda m, a: Markup(
            '<br>'.join(m.operator)),
        Movie.composer: lambda m, a: Markup(
            '<br>'.join(m.composer)),
        Movie.actors: lambda m, a: Markup(
            '<br>'.join(m.actors)),
        Movie.editor: lambda m, a: Markup(
            '<br>'.join(m.editor)), }

    # список отображаемых полей из модели
    column_list = '__all__'

    # список полей по которым разрешен поиск
    column_searchable_list = [c.name for c in Movie.__table__.c]

    # список полей по которым разрешена сортировка
    column_sortable_list = [c.name for c in Movie.__table__.c]

    # поле с сортировкой по умолчанию
    column_default_sort = [(Movie.title, True)]

    # переименование исходных заголовков столбцов
    column_labels = {Movie.id: "id", Movie.url: "Ссылка",
                     Movie.title: "Название",
                     Movie.eng_title: "Название на английском",
                     Movie.description: "Краткая информация",
                     Movie.avatar: "Аватар", Movie.release_year: "Дата выхода",
                     Movie.director: "Режиссер", Movie.country: "Страна",
                     Movie.part: "Часть", Movie.duration: "Продолжительность",
                     Movie.age_restriction: "Возрастное ограничение",
                     Movie.category_id: "Категория", Movie.genres_link: "Жанр",
                     Movie.updated_at: "Дата обновления записи",
                     Movie.producer: "Продюсер", Movie.operator: "Оператор",
                     Movie.screenwriter: "Сценарист", Movie.editor: "Монтаж",
                     Movie.composer: "Композитор", Movie.actors: "Актеры",
                     Movie.created_at: "Дата создания записи",
                     }

    # имя таблицы в единственном числе
    name = "фильм:"

    # имя таблицы во множественном числе
    name_plural = "Фильмы"

    # иконка для отображения в меню
    icon = "fa-solid fa-film"


class ActorAdmin(ModelView, model=Actor):
    def empty_formatter(value: any) -> str:
        """Возвращает '-' для `None` значений"""
        return "-"

    # базовая настройка отображения None,{},[] в Form list
    column_type_formatters = {type(None): empty_formatter,
                              type({}): empty_formatter}

    # список отображаемых полей из модели
    column_list = '__all__'

    # список полей по которым разрешен поиск
    column_searchable_list = [c.name for c in Actor.__table__.c]

    # список полей по которым разрешена сортировка
    column_sortable_list = [c.name for c in Actor.__table__.c]

    # поле с сортировкой по умолчанию
    column_default_sort = [(Actor.id, True)]

    # переименование исходных заголовков столбцов
    column_labels = {Actor.id: "id", Actor.first_name: "Имя",
                     Actor.last_name: "Фамилия",
                     Actor.eng_full_name: "Полное имя на английском",
                     Actor.biography: "Биография",
                     Actor.avatar: "Аватар", Actor.height: "Возраст",
                     Actor.date_of_birth: "Дата рождения",
                     Actor.place_of_birth: "Место рождения",
                     Actor.updated_at: "Дата обновления записи",
                     Actor.created_at: "Дата создания записи"}

    form_widget_args = {'date_of_birth': {'placeholder': 'пример: 1980-01-01'}
        , 'first_name': {'required': False, }}

    # имя таблицы в единственном числе
    name = "актер"

    # имя таблицы во множественном числе
    name_plural = "Актеры"

    # иконка для отображения в меню
    icon = "fa-solid fa-star"


class NewsAdmin(ModelView, model=News):
    def empty_formatter(value: any) -> str:
        """Возвращает '-' для `None` значений"""
        return "-"

    # базовая настройка отображения None,{},[] в Form list
    column_type_formatters = {type(None): empty_formatter,
                              type({}): empty_formatter}

    # список отображаемых полей из модели
    column_list = '__all__'

    # список полей по которым разрешен поиск
    column_searchable_list = [c.name for c in News.__table__.c]

    # список полей по которым разрешена сортировка
    column_sortable_list = [c.name for c in News.__table__.c]

    # поле с сортировкой по умолчанию
    column_default_sort = [(News.created_at, True)]

    # переименование исходных заголовков столбцов
    column_labels = {News.id: "id", News.title: "Заголовок",
                     News.sub_title: "Подзаголовок",
                     News.text_news: "Содержание", News.comment: "Комментарии",
                     News.source: "Источник",
                     News.updated_at: "Дата обновления записи",
                     News.created_at: "Дата создания записи"}

    # имя таблицы в единственном числе
    name = "новость"

    # имя таблицы во множественном числе
    name_plural = "Новости"

    # иконка для отображения в меню
    icon = "fa-solid fa-newspaper"


class GenreAdmin(ModelView, model=Genre):
    def empty_formatter(value: any) -> str:
        """Возвращает '-' для `None` значений"""
        return "-"

    # базовая настройка отображения None,{},[] в Form list
    column_type_formatters = {type(None): empty_formatter,
                              type({}): empty_formatter}

    # список отображаемых полей из модели
    column_list = [Genre.id, Genre.name]

    # список исключаемых полей в отображении на детальном просмотре
    # конкретного поля
    column_details_exclude_list = [Genre.movies_link]

    # список полей по которым разрешен поиск
    column_searchable_list = [c.name for c in Genre.__table__.c]

    # список полей по которым разрешена сортировка
    column_sortable_list = [c.name for c in Genre.__table__.c]

    # поле с сортировкой по умолчанию
    column_default_sort = [(Genre.name, True)]

    # переименование исходных заголовков столбцов
    column_labels = {Genre.id: "id", Genre.name: "Название жанра",
                     Genre.updated_at: "Дата обновления записи",
                     Genre.created_at: "Дата создания записи"
                     }

    # имя таблицы в единственном числе
    name = "жанр"

    # имя таблицы во множественном числе
    name_plural = "Жанры"

    # иконка для отображения в меню
    icon = "fa-solid fa-masks-theater"
