function deleteNote(noteId) {
  fetch("/deleteNote", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ noteId: noteId }), // Send the note ID as a JSON object
  }).then((_res) => {
    window.location.href = "/";
  });
}
