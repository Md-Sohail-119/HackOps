// List of all possible emotion classes
const emotionClasses = ["joy", "sadness", "anger", "fear", "surprise", "love", "neutral"];

/**
 * Updates the background theme based on the detected emotion.
 * @param {string} emotion - The detected emotion (e.g., "joy", "sadness", or "reset").
 */
function changeTheme(emotion) {
    const body = document.body;

    // First, remove any existing emotion classes from the body
    body.classList.remove(...emotionClasses);

    // Add the new emotion class if it's a valid one
    if (emotionClasses.includes(emotion)) {
        body.classList.add(emotion);
        console.log(`Theme changed to: ${emotion}`);
    } else {
        // If the emotion is "reset" or unknown, it will default to the image background
        // because all emotion classes have been removed.
        console.log(`Theme reset to default.`);
    }
}