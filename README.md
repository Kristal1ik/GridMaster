# GridMaster: Интерпретатор для Двумерного Перемещения

## Описание

GridMaster - это интерпретатор для выполнения команд двумерного перемещения, представленных в текстовом файле. Программа поддерживает различные команды, такие как `SET`, `IFBLOCK`, `ENDIF`, `REPEAT`, `ENDREPEAT`, `PROCEDURE`, `ENDPROC`, `CALL`. Интерпретатор обеспечивает обработку ошибок и вывод соответствующих сообщений.

## Требования

- Windows 7 или выше

## Установка и Запуск

1. Скачайте архив с программой [GridMaster.zip](#https://drive.google.com/drive/folders/1QQeTI4cuKCvtdeR1eYdMvKgQ-sfM1x9J?usp=sharing).

2. Распакуйте архив в удобное для вас место.

3. Запустите `GridMaster.exe`.

4. Взаимодействуйте с программой через графический интерфейс.

## Файл Программы

Пример файла программы (`test.txt`):

```plaintext
SET X = 2
REPEAT X
    RIGHT 5
ENDREPEAT
DOWN 10
PROCEDURE MoveLeftAndUp
    LEFT 2
    UP 2
ENDPROC
CALL MoveLeftAndUp
