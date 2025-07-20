# MeetScribe

A mobile app for recording, transcribing, and managing face-to-face meetings.

## Core Concept

MeetScribe acts as an intelligent replacement for a standard voice recorder. It allows users to easily record in-person meetings, send the audio for automatic transcription, and then review both the audio and the transcribed text in one place.

## Key Features

### 1. User Authentication
-   Secure user login to access personal meeting data.
-   A simple registration process for new users.

### 2. Meeting Dashboard
-   **Primary View:** Displays a list of all past meetings.
-   **Data Fetching:** Pulls meeting details (title, date, audio link, transcription status) from an API.
-   **Filtering:** Users can filter the meeting list by date (e.g., Today, Last 7 Days, Custom Range).
-   **Playback:** An integrated audio player allows users to listen to any meeting's recording directly from the list.

### 3. Recording & Processing
-   **Record:** A simple, one-tap interface to start and stop recording a new meeting.
-   **Save & Upload:** Upon stopping the recording, the app saves the audio file locally and immediately pushes it to a designated API endpoint for transcription processing.
-   **Status Indicator:** The meeting list shows a "transcribing..." status until the text is ready.

### 4. Transcription Viewer
-   **Data Fetching:** The app periodically checks the API for completed transcriptions.
-   **Display:** Once a transcription is available, the user can tap on the meeting to view the full text.
-   **Synchronization (Optional Enhancement):** Highlight text as the audio plays back.

## API Interaction Summary

-   `POST /login` - User authentication.
-   `GET /meetings` - Fetch the list of meetings for the logged-in user.
-   `POST /meetings/upload` - Push a new audio file for transcription.
-   `GET /meetings/{id}/transcription` - Pull the completed transcription text for a specific meeting.
