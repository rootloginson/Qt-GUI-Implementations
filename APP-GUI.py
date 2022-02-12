from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic
from src import demo_get_track
from src.custom_exception_check import trigger_starttime_log
from src.database import update_db


class StatusVisual:
    @staticmethod
    def empty_label(other):
        other.setText("Empty")
        other.setStyleSheet("")

    @staticmethod
    def pending_label(other):
        other.setText(" Pending ")
        other.setStyleSheet("background-color: rgb(255, 170, 0); color:rgb(0, 0, 0);")

    @staticmethod
    def accepted_label(other):
        other.setText(" Accepted ")
        other.setStyleSheet("background-color: #61ffb5; color:rgb(0, 0, 0);")

    @staticmethod
    def failed_label(other):
        other.setText(" Failed ")
        other.setStyleSheet("background-color: #ff574b; color:rgb(255, 255, 255);")

    @staticmethod
    def retrieve_track_button(other):
        """If the retrieving track process takes time"""
        other.setStyleSheet("background-color: #bfd7e3; color:rgb(0, 0, 0);")
        other.setText("Retrieving...")

    @staticmethod
    def finalized_track_button(other):
        other.setStyleSheet("")
        other.setText("Turn the Wheel")


class UI(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("qt-user-interface/get_random_track_user_interface.ui", self)

                ### Initialize: Authorization Attributes ###
        self.client_id = None
        self.client_secret = None
        self.client_credential_access_token = None

        # Set  : test_confirmation_status
        self.test_confirmation_status = False

                ### Initialize: GUI Variables ###

        # Disable  :  button  :  "Test_Now".
        self.pushButton_test_now.setEnabled(False)

        # Hide  :  widget :  retrieve_track_widget
        self.retrieve_track_widget.hide()

        # button connections of auth
        self.auth_button_connections()

    def auth_button_connections(self):
        # "Confirm" button of Client ID
        self.pushButton_client_id_confirm.clicked.connect(self.btn_clicked_authorization_client_id_confirm)

        # "Confirm" of Client Secret
        self.pushButton_client_secret_confirm.clicked.connect(self.btn_clicked_authorization_client_secret_confirm)

        # "Reset" button
        self.pushButton_client_reset.clicked.connect(self.btn_clicked_authorization_client_reset)

        # "Test Now" button
        self.pushButton_test_now.clicked.connect(self.btn_clicked_authorization_test_now)

        # "Retrieve Track" button
        # "Turn the Wheel" button
        # The label name of the "Retrieve Track" button was later
        # changed to the label name "Turn the Wheel".
        self.pushButton_retrieve_track.clicked.connect(self.btn_clicked_retrieve_track)

    def reset_authorization_attributes(self):
        self.client_id = None
        self.client_secret = None
        self.test_confirmation_status = False
        self.client_credential_access_token = None

    # "Confirm" button of Client ID
    def btn_clicked_authorization_client_id_confirm(self):
        # Get  :  lineEdit  :  Text  : lineEdit: "Client ID"
        # Set  :  instance variable  : "client_id"
        textInput = self.lineEdit_client_id.text()
        self.client_id = textInput

        # Disable  :  button    :  "Confirm".
        # Modify   :  lineEdit  :  "Client ID".
        self.pushButton_client_id_confirm.setEnabled(False)
        self.lineEdit_client_id.setEnabled(False)

        # Enable          :  button  :  "Test Now".
        # Modify Visuals  :  label   :  Client "Status"
        if self.client_secret and self.client_id:
            StatusVisual.pending_label(self.label_client_status_active)
            self.pushButton_test_now.setEnabled(True)

    # "Confirm" button of Client Secret
    def btn_clicked_authorization_client_secret_confirm(self):
        # Get  :  lineEdit  :  Text  :  "Client Secret".
        # Set  :  instance variable  :  "client_secret".
        textInput = self.lineEdit_client_secret.text()
        self.client_secret = textInput

        # Disable  :  button    :  "Confirm".
        # Modify   :  lineEdit  :  "Client Secret".
        self.pushButton_client_secret_confirm.setEnabled(False)
        self.lineEdit_client_secret.setEnabled(False)

        # Enable          :  button  :  "Test Now".
        # Modify Visuals  :  label   :  Client "Status"
        if self.client_secret and self.client_id:
            StatusVisual.pending_label(self.label_client_status_active)
            self.pushButton_test_now.setEnabled(True)

    # "Reset" button
    def btn_clicked_authorization_client_reset(self):
        # Reset  :  instance variables  : "client_id" and "client_secret" and "test_confirmation_status"
        self.reset_authorization_attributes()

        # Modify Visuals  :  label  :  "Status".
        StatusVisual.empty_label(self.label_client_status_active)

        # Modify Visuals:  lineEdit  :  "Client ID" and "Client Secret".
        self.lineEdit_client_id.setText("")
        self.lineEdit_client_secret.setText("")
        self.lineEdit_client_id.setEnabled(True)
        self.lineEdit_client_secret.setEnabled(True)

        # Modify Visuals  :  label  :  "Test Now"
        StatusVisual.empty_label(self.label_test_now)

        # Disable  :  button  :  "Test Now".
        # Enable   :  button  :  "Confirm" button of "Client Secret"
        # Enable   :  button  :  "Confirm" button of "Client ID".
        self.pushButton_test_now.setEnabled(False)
        self.pushButton_client_id_confirm.setEnabled(True)
        self.pushButton_client_secret_confirm.setEnabled(True)

        # Modify  :  label  :  retrieve_track_artist etc.
        # Hide    :  widget :  retrieve_track_widget
        self.reset_track_info_labels()
        self.retrieve_track_widget.hide()

    # "Test Now" button
    def btn_clicked_authorization_test_now(self):
        r = demo_get_track.gui_auth_check(self.client_id, self.client_secret)

        if r is None:
            self.auth_failed_status_call()
        elif r.status_code == 200:
            # Set : instance variable : client_credential_access_token
            self.client_credential_access_token = r.json()['access_token']
            self.auth_succession_status_call()
        else:
            self.auth_failed_status_call()

    def auth_succession_status_call(self):
        """Updates visuals if authorization is successful."""
        labels = (
            self.label_client_status_active,
            self.label_test_now
        )
        # Modify Visuals  :  label  :  "Test Now", Client "Status"
        _ = list(map(StatusVisual.accepted_label, labels))

        # Disable  :  button  :  "Test Now".
        self.pushButton_test_now.setEnabled(False)

        # Set  :  instance variable  :  test_confirmation_status
        self.test_confirmation_status = True

        # Show  :  widget :  retrieve_track_widget
        self.reset_track_info_labels()
        self.retrieve_track_widget.show()

    def auth_failed_status_call(self):
        """Updates visuals if authorization fails."""
        labels = (
            self.label_client_status_active,
            self.label_test_now
        )
        # Modify Visuals  :  label  :  "Test Now", Client "Status"
        _ = list(map(StatusVisual.failed_label, labels))

        # Set  :  instance variable  :  test_confirmation_status
        self.test_confirmation_status = False

    # Get Random Track
    def btn_clicked_retrieve_track(self):
        if self.test_confirmation_status:
            # if test is successful
            received_track_details = demo_get_track.run_spotify_app(self.client_credential_access_token)

            if isinstance(received_track_details, dict):  # a defensive control
                StatusVisual.retrieve_track_button(self.pushButton_retrieve_track)
                self.set_track_info_labels(received_track_details)
                StatusVisual.finalized_track_button(self.pushButton_retrieve_track)
                # update the database
                update_db(received_track_details)
            else:
                self.auth_failed_status_call()

    def reset_track_info_labels(self):
        self.label_retrieve_track_artist.setText('Artist')
        self.label_retrieve_track_album.setText('Album')
        self.label_retrieve_track_song.setText('Song')
        self.label_retrieve_track_url.setText('Url')
        self.label_retrieve_track_url.setOpenExternalLinks(False)

    def set_track_info_labels(self, d: dict):
        """
        received_track_details = {
            'artist_name': None,
            'album_name': None,
            'track_name': None,
            'track_external_urls': None,
            'track_uri': None
        }
        """
        self.label_retrieve_track_artist.setText(d['artist_name'])
        self.label_retrieve_track_album.setText(d['album_name'])
        self.label_retrieve_track_song.setText(d['track_name'])
        self.label_retrieve_track_url.setText(f'<a href="{d["track_external_urls"]}">{d["track_external_urls"]}</a>')
        self.label_retrieve_track_url.setOpenExternalLinks(True)


def startApp():
    import sys

    # adds approximate function call time(GMT 0:00 format) to log file.
    trigger_starttime_log("Spotify App executed")

    app = QApplication(sys.argv)
    myapp = UI()
    myapp.show()
    exit_val = app.exec_()

    trigger_starttime_log(f"Spotify App terminated. exit_val={exit_val}")
    sys.exit(exit_val)


if __name__ == "__main__":
    startApp()
