from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.init_db import get_db
from app.crud.crud_news import NewsCRUD
from app.schemas.News import NewsCreateSchema
from app.utils.form_news import form_news_data_main_page, parse_form_data, form_news_data_news_page
from app.utils.logging import AppLogger

logger = AppLogger().get_logger()

router = APIRouter()


@router.post(
    path="/add_news",
    summary="Добавить новость",
    response_description="Добавленная новость",
    status_code=status.HTTP_201_CREATED,
)
async def add_news(
        session: AsyncSession = Depends(get_db),
        form_data: dict = Depends(parse_form_data)
):
    try:
        # Проверка на существующую новость
        existing_news = await NewsCRUD.get_news(session, title=form_data.get("title"))
        if existing_news:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Новость с таким названием уже существует.",
            )

        # Создаем объект схемы Pydantic
        new_news_data = NewsCreateSchema(**form_data)

        # Создаем новость
        new_news = await NewsCRUD.create_news(session, new_news_data)
        if not new_news:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ошибка при создании новости, попробуйте еще раз...",
            )

        logger.info("Новость %s успешно добавлен", new_news.title)

        return JSONResponse(
            status_code=201,
            content={
                "success": True,
                "data": form_news_data_main_page([new_news])[0]
            }
        )

    except HTTPException as e:
        logger.error("Ошибка при добавлении новости: %s", e.detail)
        raise e
    except Exception as e:
        logger.error("Ошибка при добавлении новости: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка сервера. Попробуйте позже.",
        )


@router.get(
    path="/get_news_main_page",
    summary="Получить все новости для главной страницы",
    response_description="Список новостей для главной страницы"
)
async def get_news_main_page(session: AsyncSession = Depends(get_db)):
    news_list = await NewsCRUD.get_all_news(session)
    return JSONResponse(
        status_code=200,
        content={"news": form_news_data_main_page(news_list)}
    )


@router.get(
    path="/get_news_news_page",
    summary="Получить все новости для страницы новостей",
    response_description="Список новостей для новостной страницы"
)
async def get_news_news_page(session: AsyncSession = Depends(get_db)):
    news_list = await NewsCRUD.get_all_news(session)
    return JSONResponse(
        status_code=200,
        content={"news": form_news_data_news_page(news_list)}
    )


@router.delete(
    path="/delete_news",
    summary="Удалить новость",
    response_description="Удаленная новость"
)
async def delete_news(session: AsyncSession = Depends(get_db),
                      news_id: int = Form(...)):
    try:
        deleted = await NewsCRUD.delete_news(session, id=news_id)
        if deleted:
            logger.info("Новость %s удалена", id=news_id)
            return JSONResponse(status_code=200, content={"message": f"Новость '{news_id}' успешно удалена."})
        else:
            logger.info("Новость %s не найдена", news_id)
            return JSONResponse(status_code=404, content={"error": "Новость не найдена."})

    except Exception as exc:
        logger.error('Ошибка при удалении новости: %s', exc)
        return JSONResponse(status_code=500, content={"error": "Внутренняя ошибка сервера"})
