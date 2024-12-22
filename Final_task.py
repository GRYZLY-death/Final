import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sqlite3

# Файл сохраняется локально на ПК, изучаем глазами, данные из него кладём в таблицу базы данных и дальше работаем с ней
# Путь
file_path = r'D:\PythonProject\Steam_2024_bestRevenue_1500.csv'
# Загрузка данных из CSV файла
data = pd.read_csv(file_path)
# Удаление столбца 'steamId', как ненужного для анализа
data_cleaned = data.drop(columns=['steamId'])
# Подключение к базе данных SQLite
conn = sqlite3.connect("steam_games.db")
# Сохранение данных в таблицу 'games' в SQLite (если таблица уже существует, она будет заменена)
data_cleaned.to_sql('games', conn, if_exists='replace', index=False)
# Закрытие соединения с базой данных
conn.commit()
conn.close()
print("Данные успешно сохранены в таблице 'games' в базе данных SQLite.")

#Подключение
conn = sqlite3.connect("steam_games.db")
# Загрузка данных из таблицы 'games'
data = pd.read_sql_query("SELECT * FROM games", conn)
# Закрытие соединения
conn.close()
# Создание графиков на одной странице
plt.figure(figsize=(16, 12))

'''DI 1 На матрице корреляций для всей таблице не видно взаимосвязей (все около 0), 
однако при сосставлении корреляций для каждой категории игр закономерности видны'''
#Корреляция для всех данных
plt.subplot(2, 2, 1)
correlation_all = data.corr(numeric_only=True)  # Корреляционная матрица для всех данных
sns.heatmap(correlation_all, annot=True, fmt=".2f", cmap='coolwarm')
plt.title('Корреляционная матрица для всех игр')

# Корреляция для AAA
aaa_data = data[data['publisherClass'] == 'AAA']
plt.subplot(2, 2, 2)
correlation_aaa = aaa_data.corr(numeric_only=True)  # Корреляционная матрица для AAA
sns.heatmap(correlation_aaa, annot=True, fmt=".2f", cmap='coolwarm')
plt.title('Корреляционная матрица для ААА игр')

# Корреляция для AA
aa_data = data[data['publisherClass'] == 'AA']
plt.subplot(2, 2, 3)
correlation_aa = aa_data.corr(numeric_only=True)  # Корреляционная матрица для AA
sns.heatmap(correlation_aa, annot=True, fmt=".2f", cmap='coolwarm')
plt.title('Корреляционная матрица для АА игр')

# Корреляция для Indie
indie_data = data[data['publisherClass'] == 'Indie']
plt.subplot(2, 2, 4)
correlation_indie = indie_data.corr(numeric_only=True)  # Корреляционная матрица для Indie
sns.heatmap(correlation_indie, annot=True, fmt=".2f", cmap='coolwarm')
plt.title('Корреляционная матрица для Инди игр')

# Упаковывает все графики
plt.tight_layout()
plt.show()

'''DI 2 Топ 5 по выручке игр категории ААА заработали суммарно больше всех остальных вместе взятых'''

# Подключение к базе данных
conn = sqlite3.connect("steam_games.db")
# Загрузка данных из таблицы 'games'
data = pd.read_sql_query("SELECT name, revenue FROM games", conn)
# Закрытие соединения
conn.close()
# Получение топ-10 игр с максимальной выручкой
top_10_games = data.nlargest(10, 'revenue')
# Подсчет общей выручки всех игр
total_revenue = data['revenue'].sum()
# Подсчет выручки топ-10 игр
top_10_revenue = top_10_games['revenue'].sum()
# Вычисление выручки остальных игр
remaining_revenue = total_revenue - top_10_revenue
# Создание DataFrame для графика пирог
revenue_distribution = pd.DataFrame({
    'Name': top_10_games['name'].tolist() + ['Other Games'],
    'Revenue': top_10_games['revenue'].tolist() + [remaining_revenue]
})
# Показать подготовленные данные
print(revenue_distribution)
# Построение графика - пирог
plt.figure(figsize=(12, 8))
# Раскрашиваем палитра Husl обеспечивает разнообразные цвета
colors = sns.color_palette("husl", len(revenue_distribution))

plt.pie(revenue_distribution['Revenue'],
        labels=revenue_distribution['Name'],
        autopct='%1.1f%%',
        startangle=140,
        colors=colors)

plt.title('Распределение доходов от 10 лучших игр')
# Для кругового графика
plt.axis('equal')
plt.show()

# Сохранение данных в таблицу 'revenue_distribution'
conn = sqlite3.connect("steam_games.db")
revenue_distribution.to_sql('revenue_distribution', conn, if_exists='replace', index=False)
conn.close()

print("Данные успешно сохранены в таблице 'revenue_distribution' в базе данных.")


'''DI 3 Топ 5 по выручке игр категории ААА заработали суммарно больше всех остальных вместе взятых'''
# Подключение к базе данных
conn = sqlite3.connect("steam_games.db")
# Загрузка данных из таблицы 'games'
data = pd.read_sql_query("SELECT publisherClass, revenue FROM games", conn)
# Закрытие соединения
conn.close()

# Анализ данных по классу игр
# Фильтрация данных для каждой категории
aaa_games = data[data['publisherClass'] == 'AAA']
aa_games = data[data['publisherClass'] == 'AA']
indie_games = data[data['publisherClass'] == 'Indie']

# Подсчет количества и суммарной выручки для каждой категории
aaa_count = aaa_games.shape[0]
aaa_revenue_sum = aaa_games['revenue'].sum()
aaa_revenue_per_game = aaa_revenue_sum / aaa_count if aaa_count else 0

aa_count = aa_games.shape[0]
aa_revenue_sum = aa_games['revenue'].sum()
aa_revenue_per_game = aa_revenue_sum / aa_count if aa_count else 0

indie_count = indie_games.shape[0]
indie_revenue_sum = indie_games['revenue'].sum()
indie_revenue_per_game = indie_revenue_sum / indie_count if indie_count else 0

# Общие значения
total_games = len(data)
percentage_aaa = (aaa_count / total_games) * 100 if total_games > 0 else 0
percentage_aa = (aa_count / total_games) * 100 if total_games > 0 else 0
percentage_indie = (indie_count / total_games) * 100 if total_games > 0 else 0

# Подготовка данных для визуализации
revenues = [aaa_revenue_sum, aa_revenue_sum, indie_revenue_sum]
percentages = [percentage_aaa, percentage_aa, percentage_indie]
labels_revenue = ['AAA', 'AA', 'Indie']

# Подготовка данных для сохранения
summary_data = pd.DataFrame({
    'Publisher Class': ['AAA', 'AA', 'Indie'],
    'Count': [aaa_count, aa_count, indie_count],
    'Total Revenue': [aaa_revenue_sum, aa_revenue_sum, indie_revenue_sum],
    'Average Revenue per Game': [aaa_revenue_per_game, aa_revenue_per_game, indie_revenue_per_game],
    'Percentage of Total Games': [percentage_aaa, percentage_aa, percentage_indie]
})

# Показать подготовленные данные
print(summary_data)

# Создание пирогового графика
plt.figure(figsize=(14, 8))

# Процентное отношение прибыли по типу publisherClass в виде пирога
plt.subplot(2, 1, 1)
plt.pie(revenues, labels=labels_revenue, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("husl", len(labels_revenue)))
plt.title('Распределение выручки по классам издателей')

# Общее количество и средняя выручка на одну игру
plt.subplot(2, 1, 2)
bar_width = 0.35
x_labels = ['AAA', 'AA', 'Indie']

# Столбчатый график для количества игр
sns.barplot(x=x_labels, y=summary_data['Count'], color='lightblue', label='Количество игр')

# Создание второй оси для средней выручки
ax2 = plt.gca().twinx()
ax2.plot(x_labels, summary_data['Average Revenue per Game'], color='orange', marker='o', label='Средний доход за игру')
ax2.set_ylabel('Средний доход за игру')

# Добавление легенды
plt.title('Количество игр и средний доход за игру')
plt.xlabel('Publisher Class')
plt.ylabel('Count of Games')
plt.legend(loc='upper left')
ax2.legend(loc='upper right')

# Подгоняет график
plt.tight_layout()
plt.show()

# Сохранение данных в таблицу 'publisher_revenue_3'
conn = sqlite3.connect("steam_games.db")
summary_data.to_sql('publisher_revenue_3', conn, if_exists='replace', index=False)
conn.close()

print("Данные успешно сохранены в таблице 'publisher_revenue_3' в базе данных.")

'''DI 4 Игр ААА выходит меньше, но средний доход игры ААА больше, ИНДИ игры наоборот'''
#Подключение к базе данных
conn = sqlite3.connect("steam_games.db")
# Загрузка данных из таблицы 'games'
data = pd.read_sql_query("SELECT publisherClass, releaseDate, revenue FROM games", conn)
# Закрытие соединения
conn.close()

# Преобразование столбца 'releaseDate' в формат даты
data['releaseDate'] = pd.to_datetime(data['releaseDate'], errors='coerce')

# Извлечение месяца и года из даты
data['releaseMonth'] = data['releaseDate'].dt.month
data['releaseYear'] = data['releaseDate'].dt.year

# Фильтрация данных для каждой категории
aaa_games = data[data['publisherClass'] == 'AAA']
aa_games = data[data['publisherClass'] == 'AA']
indie_games = data[data['publisherClass'] == 'Indie']

# Агрегация данных по месяцам
aaa_monthly_revenue = aaa_games.groupby('releaseMonth')['revenue'].sum().reset_index()
aa_monthly_revenue = aa_games.groupby('releaseMonth')['revenue'].sum().reset_index()
indie_monthly_revenue = indie_games.groupby('releaseMonth')['revenue'].sum().reset_index()

# Переименование столбцов для удобства
aaa_monthly_revenue.columns = ['Month', 'AAA Revenue']
aa_monthly_revenue.columns = ['Month', 'AA Revenue']
indie_monthly_revenue.columns = ['Month', 'Indie Revenue']

# Объединение данных
monthly_revenue = aaa_monthly_revenue.merge(aa_monthly_revenue, on='Month', how='outer')
monthly_revenue = monthly_revenue.merge(indie_monthly_revenue, on='Month', how='outer')

# Заполнение пропущенных значений нулями
monthly_revenue.fillna(0, inplace=True)

# Показать агрегированные данные
print(monthly_revenue)

# Визуализация
plt.figure(figsize=(12, 6))
sns.lineplot(data=monthly_revenue, x='Month', y='AAA Revenue', label='Доход AAA игр', marker='o')
sns.lineplot(data=monthly_revenue, x='Month', y='AA Revenue', label='Доход AA Игр', marker='o')
sns.lineplot(data=monthly_revenue, x='Month', y='Indie Revenue', label='Доход Indie Игр', marker='o')

plt.title('Ежемесячный анализ выручки по классам игр')
plt.xlabel('Месяц')
plt.ylabel('Общий доход в $')
plt.xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

# Сохранение данных в таблицу 'monthly_revenue_4'
conn = sqlite3.connect("steam_games.db")
monthly_revenue.to_sql('monthly_revenue_4', conn, if_exists='replace', index=False)
conn.close()

print("Данные успешно сохранены в таблице 'monthly_revenue_4' в базе данных.")

'''5 DI - по анализу топ 20 игр по выручке в каждой из категорий времени 
в индииграх пользователи проводят больше, хотя прибыли игры приносят меньше
'''

# Подключение к базе данных
conn = sqlite3.connect("steam_games.db")

# Загрузка данных из таблицы 'games'
data = pd.read_sql_query("SELECT publisherClass, avgPlaytime, revenue FROM games", conn)

# Закрытие соединения
conn.close()

# Получение топ-20 игр по каждой категории
top_20_aaa = data[data['publisherClass'] == 'AAA'].nlargest(20, 'revenue')
top_20_aa = data[data['publisherClass'] == 'AA'].nlargest(20, 'revenue')
top_20_indie = data[data['publisherClass'] == 'Indie'].nlargest(20, 'revenue')

# Объединение топ-20 игр в один DataFrame
top_20_combined = pd.concat([top_20_aaa, top_20_aa, top_20_indie])

# Агрегация данных для анализа
combined_agg = top_20_combined.groupby('publisherClass').agg(
    Count=('avgPlaytime', 'count'),
    AvgPlaytime=('avgPlaytime', 'mean'),
    AvgRevenue=('revenue', 'mean')
).reset_index()

# Показать подготовленные данные
print(combined_agg)

# Сохранение данных для анализа
conn = sqlite3.connect("steam_games.db")
combined_agg.to_sql('top_20_games_analysis_4', conn, if_exists='replace', index=False)
conn.close()

print("Данные успешно сохранены в таблице 'top_20_games_analysis_4' в базе данных.")

# Построение комбинированного графика
plt.figure(figsize=(12, 6))

# Столбчатая диаграмма для количества игр
bar_plot = sns.barplot(data=combined_agg, x='publisherClass', y='Count', color='lightblue')

# Подпись категорий на столбцах
for index, row in combined_agg.iterrows():
    bar_plot.text(index, row['Count'] - 10, row['publisherClass'], color='black', ha="center", va="bottom")  # Размещение названия категории над столбцом

# Создание второй оси для средней выручки
ax2 = plt.gca().twinx()
sns.lineplot(data=combined_agg, x='publisherClass', y='AvgPlaytime', ax=ax2, color='orange', marker='o')

# Создание третьей оси для средней выручки
ax3 = ax2.twinx()
sns.lineplot(data=combined_agg, x='publisherClass', y='AvgRevenue', ax=ax3, color='green', marker='o')

# Настройка графика
plt.title('Анализ 20 лучших игр в каждой из категорий')

# Установка единых осей для графика
ax2.set_ylim(0, ax2.get_ylim()[1])  # Убедитесь, что ось Y для среднего времени игры появляется с нуля
ax3.set_ylim(0, ax3.get_ylim()[1])  # Убедитесь, что ось Y для средней выручки начинается с нуля

# Устанавливаем пустые подписи осей
plt.xlabel('')
plt.ylabel('')
ax2.set_ylabel('')
ax3.set_ylabel('')

# Убираем метки осей
plt.xticks([])
ax2.set_yticks([])
ax3.set_yticks([])

# Установка единой легенды
lines = [plt.Line2D([0], [0], color='lightblue', lw=6),  # Количество игр
         plt.Line2D([0], [0], color='orange', lw=6),  # Среднее время в игре
         plt.Line2D([0], [0], color='green', lw=6)]  # Средняя выручка на игру
labels = ['Количество игр', 'Среднее время в игре (минуты)', 'Средняя выручка на игру (в $)']
plt.legend(lines, labels, loc='upper left')

plt.grid(False)  # Отключаем сетку
plt.tight_layout()  # Упаковка графиков
plt.show()