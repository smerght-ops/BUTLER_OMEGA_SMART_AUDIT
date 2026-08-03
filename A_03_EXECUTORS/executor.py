import os
import datetime
import re

class Executor:
    def __init__(self, output_dir="A_05_STORAGE"):
        self.output_dir = output_dir
        self.GREEN = "\033[92m"
        self.RESET = "\033[0m"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _clean_html(self, raw_html):
        cleanr = re.compile('<.*?>')
        return re.sub(cleanr, '', raw_html)

    def save_file(self, filename, content, category="general"):
        if not filename:
            raise ValueError("Имя файла не может быть пустым.")
        path = os.path.join(self.output_dir, filename)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        final_content = self._clean_html(content) if filename.endswith('.html') else content
        header = f"--- [SYSTEM LOG] ---\nOrigin: {category}\nTime: {timestamp}\n--------------------\n\n"
        try:
            with open(path, 'w', encoding='utf-8') as file:
                file.write(header + final_content)
            print(f"{self.GREEN}[SUCCESS] Файл {filename} заменен/создан успешно. Проверка прошла хорошо.{self.RESET}")
            return path
        except IOError as e:
            print(f"\033[91m[ERROR] Ошибка при записи файла {filename}: {e}\033[0m")
            raise

    def delete_file(self, filename):
        path = os.path.join(self.output_dir, filename)
        if os.path.exists(path):
            try:
                os.remove(path)
                print(f"{self.GREEN}[SUCCESS] Артефакт {filename} удален успешно.{self.RESET}")
            except IOError as e:
                print(f"\033[91m[ERROR] Ошибка при удалении файла {filename}: {e}\033[0m")

if __name__ == '__main__':
    ex = Executor()
    ex.save_file('test_html_cleaner.html', '<h1>Заголовок</h1><p>Текст</p>', category='Test')
    print(f"{ex.GREEN}--> [Executor] Исполнитель начал работать.{ex.RESET}")
