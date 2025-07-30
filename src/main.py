from services import search_description
from reports import spending_by_category
from utils import get_transactions_xlsx
from views import main_page


def main():
    """Основная функция для демонстрации работы программы"""

    print(main_page("2025-07-30 18:37:56"))
    data = get_transactions_xlsx("../data/operations.xlsx")
    category_data = spending_by_category(data, "Переводы", "31.12.2021")
    print(category_data["Категория"], "\n")
    search_data = search_description("Ozon.ru", data)
    print(search_data["Описание"])


if __name__ == "__main__":
    main()
