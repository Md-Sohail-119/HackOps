const themeSwitcher = {
    emotionClasses: ["joy", "sadness", "anger", "fear", "surprise", "love", "neutral"],
    currentEmotion: null,
    body: document.body,

    change(emotion) {
        const previousEmotion = this.currentEmotion;

        if (emotion === previousEmotion) {
            return;
        }

        if (previousEmotion) {
            this.body.classList.remove(previousEmotion);
        }

        if (this.emotionClasses.includes(emotion)) {
            if (previousEmotion) {
                this.body.style.backgroundImage = `url('${previousEmotion}.png')`;
            } else {
                this.body.style.backgroundImage = `url('Screenshot_HomePage.png')`;
            }
            this.body.classList.add(emotion);
            this.currentEmotion = emotion;
            console.log(`Theme changed to: ${emotion}`);
        } else {
            this.body.style.backgroundImage = `url('Screenshot_HomePage.png')`;
            this.currentEmotion = null;
            console.log(`Theme reset to default.`);
        }
    }
};

// Make the function globally accessible for the inline `onclick` attributes
function changeTheme(emotion) {
    themeSwitcher.change(emotion);
}

const musicPlayer = {
    currentlyPlaying: null,
    progressIntervals: [],
    songCards: document.querySelectorAll('.song-card'),

    togglePlay(card, index) {
        if (this.currentlyPlaying !== null && this.currentlyPlaying !== index) {
            this.stopSong(this.currentlyPlaying);
        }

        if (this.currentlyPlaying === index) {
            this.stopSong(index);
            this.currentlyPlaying = null;
        } else {
            this.playSong(card, index);
            this.currentlyPlaying = index;
        }
    },

    playSong(card, index) {
        const playButton = card.querySelector('.play-button');
        const progressFill = card.querySelector('.progress-fill');

        playButton.textContent = '⏸️';
        playButton.classList.add('playing');
        card.classList.add('playing');

        // Update emotion box based on song
        this.updateEmotionBox(index);

        let progress = 0;
        this.progressIntervals[index] = setInterval(() => {
            progress += 0.5;
            progressFill.style.width = progress + '%';

            if (progress >= 100) {
                this.stopSong(index);
                this.currentlyPlaying = null;
            }
        }, 150);
    },

    stopSong(index) {
        if (index < 0 || index >= this.songCards.length) return;
        const card = this.songCards[index];
        if (!card) return; // Extra safety check

        const playButton = card.querySelector('.play-button');
        const progressFill = card.querySelector('.progress-fill');

        playButton.textContent = '▶️';
        playButton.classList.remove('playing');
        card.classList.remove('playing');

        if (this.progressIntervals[index]) {
            clearInterval(this.progressIntervals[index]);
            this.progressIntervals[index] = null;
        }

        setTimeout(() => {
            if (progressFill) {
                progressFill.style.width = '0%';
            }
        }, 500);
    },

    updateEmotionBox(songIndex) {
        const emotionBox = document.getElementById('emotionBox');
        const emotionIcon = emotionBox.querySelector('.emotion-icon');
        const emotionTitle = emotionBox.querySelector('h3');
        const emotionText = emotionBox.querySelector('p');
        
        const emotions = [
            {
                icon: '🌙',
                title: 'Feeling Dreamy & Reflective',
                text: 'This midnight melody perfectly captures those late-night thoughts and peaceful moments of introspection.'
            },
            {
                icon: '⚡',
                title: 'Energized & Electric',
                text: 'These electric vibes are pumping up your energy and getting you ready to take on any challenge!'
            },
            {
                icon: '🕺',
                title: 'Ready to Dance & Move',
                text: 'The rhythm is calling your soul to move! Perfect for when you need to shake off stress and feel alive.'
            },
            {
                icon: '🌅',
                title: 'Nostalgic & Warm',
                text: 'This golden hour sound brings back beautiful memories and fills your heart with warmth and hope.'
            },
            {
                icon: '☔',
                title: 'Smooth & Contemplative',
                text: 'Like gentle rain, this jazz soothes your mind and creates the perfect atmosphere for deep thinking.'
            }
        ];
        
        const emotion = emotions[songIndex];
        emotionIcon.textContent = emotion.icon;
        emotionTitle.textContent = emotion.title;
        emotionText.textContent = emotion.text;
    },
};

// Make the function globally accessible for the inline `onclick` attributes
function togglePlay(card, index) {
    musicPlayer.togglePlay(card, index);
}

function goHome() {
    // Stop any currently playing song
    if (musicPlayer.currentlyPlaying !== null) {
        musicPlayer.stopSong(musicPlayer.currentlyPlaying);
        musicPlayer.currentlyPlaying = null;
    }
    
    // Reset emotion box to default
    const emotionBox = document.getElementById('emotionBox');
    const emotionIcon = emotionBox.querySelector('.emotion-icon');
    const emotionTitle = emotionBox.querySelector('h3');
    const emotionText = emotionBox.querySelector('p');
    
    emotionIcon.textContent = '🎭';
    emotionTitle.textContent = 'This Playlist Suits Your Current Vibe';
    emotionText.textContent = 'These carefully curated tracks are perfect for your emotional journey right now - from dreamy reflections to energetic bursts.';
    
    // Scroll to top smoothly
    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Navigate to home page after a short delay to allow animations to settle
    setTimeout(() => {
        window.location.href = 'index.html';
    }, 300);
}