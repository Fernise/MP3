import sys, os
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QLineEdit, QFormLayout
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

import eyed3

class MP3(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("MP3")
        self.window_width = 480
        self.window_height = 340
        self.setMinimumSize(self.window_width, self.window_height)

        # Layout: botón play
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Widgets: boton play
        button_play = QPushButton('Play')
        button_play.clicked.connect(self.PlayAudioFile)
        self.layout.addWidget(button_play)

        # Layout: botones '+', '-', 'Pause', 'Unpause'
        volume_control = QHBoxLayout()
        self.layout.addLayout(volume_control)

        # Widgets: botones '+', '-', 'Pause', 'Unpause'
        button_crank_up = QPushButton('+')
        button_crank_up.clicked.connect(self.CrankUp)

        button_crank_down = QPushButton('-')
        button_crank_down.clicked.connect(self.CrankDown)

        button_pause = QPushButton('Pause')
        button_pause.clicked.connect(self.Pause)

        button_unpause = QPushButton('Unpause')
        button_unpause.clicked.connect(self.Unpause)

        # Se añaden los botones al layout
        volume_control.addWidget(button_crank_up)
        volume_control.addWidget(button_crank_down)
        volume_control.addWidget(button_pause)
        volume_control.addWidget(button_unpause)

        # Metadatos
        self.audio_data = eyed3.load("test.mp3")

        # Metadatos: artista
        self.artist_label = QLabel(self.audio_data.tag.artist)
        self.artist_text_line = QLineEdit()
        self.artist_text_line.setPlaceholderText("Introduzca el nombre del artista: ")
        self.artist_text_line.returnPressed.connect(self.ChangeArtist)

        # Metadatos: album
        self.album_label = QLabel(self.audio_data.tag.album)
        self.album_text_line = QLineEdit()
        self.album_text_line.setPlaceholderText("Introduzca el nombre del álbum: ")
        self.album_text_line.returnPressed.connect(self.ChangeAlbum)

        # Metadatos: título
        self.title_label = QLabel(self.audio_data.tag.title)
        self.title_text_line = QLineEdit()
        self.title_text_line.setPlaceholderText("Introduzca el título de la canción: ")
        self.title_text_line.returnPressed.connect(self.ChangeTitle)

        # Metadatos: número de track
        self.track_num_label = QLabel(str(self.audio_data.tag.track_num))
        self.track_num_text_line = QLineEdit()
        self.track_num_text_line.setPlaceholderText("Introduzca el número de track: ")
        self.track_num_text_line.returnPressed.connect(self.ChangeTrackNum)

        # Metadatos: género
        self.genre_label = QLabel(str(self.audio_data.tag.genre))
        self.genre_text_line = QLineEdit()
        self.genre_text_line.setPlaceholderText("Introduzca el género de la canción: ")
        self.genre_text_line.returnPressed.connect(self.ChangeGenre)

        # Metadatos: año de lanzamiento
        self.release_date_label = QLabel(str(self.audio_data.tag.release_date))
        self.release_date_text_line = QLineEdit()
        self.release_date_text_line.setPlaceholderText("Introduzca el año de lanzamiento: ")
        self.release_date_text_line.returnPressed.connect(self.ChangeReleaseDate)

        # Layout: mensaje de aviso y metadatos
        labels_layout = QFormLayout()
        self.layout.addLayout(labels_layout)

        # Mensaje de aviso
        warning_label = QLabel("Modifique los datos antes de comenzar a escuchar la canción")
        font = warning_label.font()
        font.setPointSize(15)
        warning_label.setFont(font)
        labels_layout.addWidget(warning_label)

        # Se añaden los metadatos de la canción al layout junto con la opción de modificarlos

        # Artista
        labels_layout.addRow("Artista: ", self.artist_label)
        labels_layout.addRow("Cambiar artista: ", self.artist_text_line)

        # Álbum
        labels_layout.addRow("Álbum: ", self.album_label)
        labels_layout.addRow("Cambiar álbum: ", self.album_text_line)

        # Título
        labels_layout.addRow("Título: ", self.title_label)
        labels_layout.addRow("Cambiar título: ", self.title_text_line)

        # Número de track
        labels_layout.addRow("Número de track: ", self.track_num_label)
        labels_layout.addRow("Cambiar número de track: ", self.track_num_text_line)

        # Género
        labels_layout.addRow("Género: ", self.genre_label)
        labels_layout.addRow("Cambiar género: ", self.genre_text_line)

        # Año de lanzamiento
        labels_layout.addRow("Año de lanzamiento: ", self.release_date_label)
        labels_layout.addRow("Cambiar año de lanzamiento: ", self.release_date_text_line)

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()

    # Método: subir el volumen
    def CrankUp(self):
        currentVolume = self.audio_output.volume()
        print(currentVolume)
        self.audio_output.setVolume(currentVolume + 0.1)

    # Método: bajar el volumen
    def CrankDown(self):
        currentVolume = self.audio_output.volume()
        print(currentVolume)
        self.audio_output.setVolume(currentVolume - 0.1)

    # Método: pausar la canción
    def Pause(self):
        self.player.pause()

    # Método: continuar escuchando la canción
    def Unpause(self):
        self.player.play()

    # Método: comenzar a escuchar la canción
    def PlayAudioFile(self):
        full_file_path = os.path.join(os.getcwd(), "test.mp3")
        url = QUrl.fromLocalFile(full_file_path)
        self.player.setSource(url)
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(1)
        self.player.play()

    # Método: cambia el metadato "Artista" en el archivo ".mp3" y lo refresca en la ventana
    def ChangeArtist(self):
        self.artist_label.setText(self.artist_text_line.text())
        self.audio_data.tag.artist = self.artist_text_line.text()
        self.audio_data.tag.save()

    # Método: cambia el metadato "Álbum" en el archivo ".mp3" y lo refresca en la ventana
    def ChangeAlbum(self):
        self.album_label.setText(self.album_text_line.text())
        self.audio_data.tag.album = self.album_text_line.text()
        self.audio_data.tag.save()

    # Método: cambia el metadato "Título" en el archivo ".mp3" y lo refresca en la ventana
    def ChangeTitle(self):
        self.title_label.setText(self.title_text_line.text())
        self.audio_data.tag.title = self.title_text_line.text()
        self.audio_data.tag.save()

    # Método: cambia el metadato "Número de track" en el archivo ".mp3" y lo refresca en la ventana
    def ChangeTrackNum(self):
        self.track_num_label.setText(self.track_num_text_line.text())
        self.audio_data.tag.track_num = self.track_num_text_line.text()
        self.audio_data.tag.save()

    # Método: cambia el metadato "Género" en el archivo ".mp3" y lo refresca en la ventana
    def ChangeGenre(self):
        self.genre_label.setText(self.genre_text_line.text())
        self.audio_data.tag.genre = self.genre_text_line.text()
        self.audio_data.tag.save()

    # Método: cambia el metadato "Año de lanzamiento" en el archivo ".mp3" y lo refresca en la ventana
    def ChangeReleaseDate(self):
        self.release_date_label.setText(self.release_date_text_line.text())
        self.audio_data.tag.release_date = self.release_date_text_line.text()
        self.audio_data.tag.save()

