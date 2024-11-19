from argparse import ArgumentParser
from speechkit import model_repository, configure_credentials, creds
from speechkit.stt import AudioProcessingType
import os

# Аутентификация через API-ключ.
API_KEY = 'ВАШ_ТОКЕН'
configure_credentials(
    yandex_credentials=creds.YandexCredentials(
        api_key=API_KEY
    )
)

def recognize(audio, output_file=None):
    model = model_repository.recognition_model()

    # Задайте настройки распознавания.
    model.model = 'general'
    model.language = 'ru-RU'
    model.audio_processing_type = AudioProcessingType.Full

    # Распознавание речи в указанном аудиофайле.
    result = model.transcribe_file(audio)

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            for c, res in enumerate(result):
                f.write('=' * 80 + '\n')
                f.write(f'channel: {c}\n\nraw_text:\n{res.raw_text}\n\nnorm_text:\n{res.normalized_text}\n\n')
                if res.has_utterances():
                    f.write('utterances:\n')
                    for utterance in res.utterances:
                        f.write(str(utterance) + '\n')
        print(f'Распознанный текст сохранен в файл: {output_file}')
    else:
        for c, res in enumerate(result):
            print('=' * 80)
            print(f'channel: {c}\n\nraw_text:\n{res.raw_text}\n\nnorm_text:\n{res.normalized_text}\n')
            if res.has_utterances():
                print('utterances:')
                for utterance in res.utterances:
                    print(utterance)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--audio', type=str, help='audio path', required=True)
    parser.add_argument('--output', type=str, help='output file path', required=False)

    args = parser.parse_args()

    if os.path.exists(args.audio):
        recognize(args.audio, args.output)
    else:
        print('Файл не найден.') 