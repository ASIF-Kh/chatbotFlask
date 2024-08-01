// Function to set a random background
function setRandomBackground() {
    const randomIndex = Math.floor((Math.random() * 10)+1);
    // const randomBackground = backgrounds[randomIndex];
    document.body.style.backgroundImage = `url('static/images/background${randomIndex}.jpg')`;
}

// Set a random background when the page loads
window.onload = setRandomBackground;
