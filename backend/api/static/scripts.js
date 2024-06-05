// Toggle visibility of sections
document.getElementById('btnKaggle').addEventListener('click', function() {
    document.getElementById('kaggleSection').classList.remove('hidden');
    document.getElementById('apiSection').classList.add('hidden');
    this.classList.add('active');
    document.getElementById('btnAPI').classList.remove('active');
});

document.getElementById('btnAPI').addEventListener('click', function() {
    document.getElementById('apiSection').classList.remove('hidden');
    document.getElementById('kaggleSection').classList.add('hidden');
    this.classList.add('active');
    document.getElementById('btnKaggle').classList.remove('active');
});

document.addEventListener('DOMContentLoaded', function() {
    renderSentimentOverTimeChart(defaultChartData.sentimentOverTime);
    renderSentimentPieChart(defaultChartData.sentimentPie);
    generateBubbleWordCloud(defaultChartData.wordCloud);
    createDayElementsForMonth();
});


// Event listener for form submission
document.getElementById('twitterForm').addEventListener('submit', function(e) {
    e.preventDefault();  // Prevents the default form submission action
    const username = document.getElementById('username').value;  // Gets the username from the form
    analyzeSentiment(username); 
});


// This function is called whenever the user types in the search input field.
// AJAX request to the backend endpoint (in views.py) and retrieve username
function searchUsernames(searchText) {

    // Only proceed with the search if at least 3 characters have been typed.
    if (searchText.length < 1) {
        return; 
    }

    // Send a request to the server with the search term, 
    fetch(`/api/search_usernames/?term=${encodeURIComponent(searchText)}`)
        .then(response => response.json()) 
        .then(data => {
            const dataList = document.getElementById('usernames');
            dataList.innerHTML = "";

            // For each username received from the server, create a new option element appended to the datalist.
            data.forEach((username) => {
                const option = document.createElement('option');
                option.value = username; // Set the value of the option element.
                dataList.appendChild(option); // Add the option element to the datalist.
            });
        })
        .catch(error => {
            console.error('Error fetching usernames:', error);
        });
}



// Function to send the username to the Django backend and get the sentiment analysis
function analyzeSentiment(username) {
    const loadingScreen = document.getElementById('loadingScreen');
    loadingScreen.style.display = 'flex';
    updateProgress(10); // Initial progress after starting the process

    fetch(`/api/analyze_sentiment/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',  // Set the content type of the request
        },
        body: JSON.stringify({ username: username }),  // Send the username in the request body
    })
    .then(response => {
        updateProgress(20);
        return response.json();
    })
    // Call function to display the results whilst updating the progress bar
    .then(data => {
        renderSentimentOverTimeChart(data.tweets);
        updateProgress(30);

        generateBubbleWordCloud(data.tweets);
        updateProgress(40);

        renderSentimentPieChart(data.tweets);
        updateProgress(60);

        updateContributionGraph(data.tweets);
        updateProgress(80);

        displayResults(data);
        updateProgress(100); // Complete the progress when everything is done
        setTimeout(() => { loadingScreen.style.display = 'none'; }, 500); // Hide loading after a small delay
    })
    .catch(error => {
        console.error('Error:', error);
        updateProgress(0); // reset
        loadingScreen.style.display = 'none'; 
    });
}

// Function to submit user feedback on sentiment analysis
function submitFeedback(tweetId, predictedSentiment, correctedSentiment) {
    // Package data for the POST request
    const data = {
        tweet_id: tweetId,
        predicted_sentiment: predictedSentiment,
        user_corrected_sentiment: correctedSentiment
    };

    // Send feedback data to the server
    fetch('/api/submit_feedback/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(response => response.json()) // Parse response to JSON
    .then(data => {
        alert('Feedback submitted! Thank you.'); // Alert success to user
    })
    .catch((error) => {
        console.error('Error:', error); 
    });
}


function updateProgress(percent) {
    const progressBar = document.getElementById('progress');
    progressBar.style.width = percent + '%';
}


// Function to display the results of sentiment analysis and include feedback options
function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';  // Clear any previous results

    //list of sentiment options
    const sentiments = ['admiration', 'amusement', 'anger', 'annoyance', 'approval', 'caring', 'confusion', 'curiosity', 'desire', 'disappointment', 'disapproval', 'disgust', 'embarrassment', 'excitement', 'fear', 'gratitude', 'grief', 'joy', 'love', 'nervousness', 'optimism', 'pride', 'realization', 'relief', 'remorse', 'sadness', 'surprise', 'neutral'];

    // Display each tweet, its predicted sentiment, and a dropdown for feedback
    data.tweets.forEach(tweet => {
        const tweetElement = document.createElement('div');
        tweetElement.classList.add('tweet-result');

        // the text display
        const textDisplay = document.createElement('p');
        textDisplay.innerText = `Tweet: ${tweet.text} | Sentiment: ${tweet.sentiment.subcategory}`;

        //a select element for feedback
        const sentimentSelect = document.createElement('select');
        sentimentSelect.innerHTML = `<option value="">Correct Sentiment?</option>` +
            sentiments.map(sentiment => `<option value="${sentiment}">${sentiment.charAt(0).toUpperCase() + sentiment.slice(1)}</option>`).join('');
        sentimentSelect.onchange = () => submitFeedback(tweet.id, tweet.sentiment.subcategory, sentimentSelect.value);

        // append the text display and the select element to the tweet element
        tweetElement.appendChild(textDisplay);
        tweetElement.appendChild(sentimentSelect);

        // append the tweet element to the results container
        resultsDiv.appendChild(tweetElement);
    });
}


// Defualt chart data
const defaultChartData = {
    sentimentOverTime: [
        { created_at: '2023-04-01T00:00:00Z', sentiment: { score: 0.8 } },
        { created_at: '2023-04-02T00:00:00Z', sentiment: { score: 0.6 } },
        { created_at: '2023-04-03T00:00:00Z', sentiment: { score: 0.7 } },
        { created_at: '2023-04-04T00:00:00Z', sentiment: { score: 0.2 } },
        { created_at: '2023-04-05T00:00:00Z', sentiment: { score: 0.1 } }
    ],
    sentimentPie: [
        { sentiment: { subcategory: 'joy' } },
        { sentiment: { subcategory: 'admiration' } },
        { sentiment: { subcategory: 'anger' } },
        { sentiment: { subcategory: 'disappointment' } },
        { sentiment: { subcategory: 'surprise' } }
    ],
    wordCloud: [
        { text: "Positive Positive Positive Positive Positive Positive Positive Positive Positive Positive", sentiment: { subcategory: 'joy' } },
        { text: "Inspiring Inspiring Inspiring Inspiring Inspiring Inspiring Inspiring Inspiring", sentiment: { subcategory: 'admiration' } },
        { text: "Challenging Challenging Challenging Challenging Challenging Challenging", sentiment: { subcategory: 'anger' } },
        { text: "Rewarding Rewarding Rewarding Rewarding Rewarding", sentiment: { subcategory: 'pride' } },
        { text: "Unexpected Unexpected Unexpected Unexpected", sentiment: { subcategory: 'surprise' } }
    ]
};

let sentimentOverTimeChart;

// This function to render the chart, with data 'date' and 'score' properties from views.py.
function renderSentimentOverTimeChart(sentimentData) {

    const formattedData = sentimentData.map(tweet => {
        return {
            date: new Date(tweet.created_at),
            score: tweet.sentiment.score
        };
    });

    formattedData.sort((a, b) => a.date - b.date);

    // Extract the dates and scores from the formattedData array
    const labels = formattedData.map(data => data.date.toLocaleDateString());
    const scores = formattedData.map(data => data.score);

    const ctx = document.getElementById('sentimentOverTimeChart').getContext('2d');

    if (sentimentOverTimeChart) {
        sentimentOverTimeChart.destroy();
    }
    
    const averageScore = scores.reduce((sum, score) => sum + score, 0) / scores.length;
    let lineColor;
    if (averageScore > 0.25) {
        lineColor = 'rgb(0, 128, 0)';
    } else if (averageScore < -0.25) {
        lineColor = 'rgb(255, 0, 0)'; 
    } else {
        lineColor = 'rgb(0, 0, 0)'; 
    }

    // Create the chart
    sentimentOverTimeChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Sentiment Score',
                data: scores,
                fill: false,
                borderColor: lineColor,
                tension: 0.1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: false, // Sentiment scores usually aren't always positive
                    title: {
                        display: true,
                        text: 'Sentiment Score'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                }
            },
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

function renderSentimentPieChart(sentimentData) {
    const sentimentCounts = {};
    Object.keys(sentimentColors).forEach(sentiment => {
        sentimentCounts[sentiment] = 0;
    });

    sentimentData.forEach(tweet => {
        const sentiment = tweet.sentiment.subcategory;
        if (sentiment && sentimentCounts.hasOwnProperty(sentiment)) {
            sentimentCounts[sentiment] += 1;
        } else {
            sentimentCounts['neutral'] += 1; // Count as neutral if sentiment is undefined or not in the colors list
        }
    });

    const dataForPieChart = {
        labels: Object.keys(sentimentCounts),
        datasets: [{
            label: 'Sentiment Distribution',
            data: Object.values(sentimentCounts),
            backgroundColor: Object.keys(sentimentCounts).map(sentiment => sentimentColors[sentiment]),
            hoverOffset: 4
        }]
    };
    
    const ctx = document.getElementById('sentimentPieChart').getContext('2d');
    if (window.sentimentPieChartInstance) {
        window.sentimentPieChartInstance.destroy();
    }
    
    // Instantiate a new Chart
    window.sentimentPieChartInstance = new Chart(ctx, {
        type: 'pie',
        data: dataForPieChart,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                }
            }
        }
    });
}


// Process each tweet and initialize the day in the object if it's not already there
function processSentimentData(tweets) {
    const contributionData = {};

    tweets.forEach(tweet => {
        const date = new Date(tweet.created_at).toLocaleDateString();
        const sentimentScore = tweet.sentiment.score;
        
        
        if (!contributionData[date]) {
            contributionData[date] = {
                positive: 0,
                negative: 0,
                neutral: 0
            };
        }
        
        // Increment the appropriate sentiment count
        if (sentimentScore > 0.25) {
            contributionData[date].positive++;
        } else if (sentimentScore < -0.25) {
            contributionData[date].negative++;
        } else {
            contributionData[date].neutral++;
        }
    });

    return contributionData;
}

// Modify the calender heatmap function to use the processed data
function renderContributionGraph(contributionData) {
    console.log('renderContributionGraph called with contributionData:', contributionData);
    createDayElementsForMonth(); 

    const monthContainers = document.querySelectorAll('.month');

    monthContainers.forEach(container => {
        const daysContainer = container.querySelector('.days-container');
        const monthId = container.id;

        for (let day = 1; day <= 31; day++) {
            const dayElement = daysContainer.querySelector(`#${monthId}-${day}`);

            if (dayElement) {
                const dateObj = new Date(2009, getMonthIndex(monthId), day); // Assuming the year is 2009 cause thats the good chunk of kaggle data
                const dateString = dateObj.toLocaleDateString();
                const sentiments = contributionData[dateString];

                /*
                console.log('Day Element:', dayElement);
                console.log('Date String:', dateString);
                console.log('Sentiments:', sentiments);
                */

                if (sentiments) {
                    const dominantSentiment = Object.keys(sentiments).reduce((a, b) => sentiments[a] > sentiments[b] ? a : b);
                    //console.log('Dominant Sentiment:', dominantSentiment);
                    //console.log('Color:', getColorForSentiment(dominantSentiment));
                    dayElement.style.backgroundColor = getColorForSentiment(dominantSentiment);
                } else {
                    //console.log('No sentiment data for the day. Setting default color.');
                    dayElement.style.backgroundColor = '#5b5b5b'; // Default grey color for days without sentiment data
                }
            } else {
                console.log('Day element not found for:', `${monthId}-${day}`);
            }
        }
    });
}

function getMonthIndex(monthId) {
    const monthNames = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'];
    return monthNames.indexOf(monthId);
}


function createDayElementsForMonth() {
    console.log('Creating day elements for each month...');

    const daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    const monthContainers = document.querySelectorAll('.month .days-container');

    // Check for leap year and adjust February days.
    const year = new Date().getFullYear();
    if ((year % 4 === 0 && year % 100 !== 0) || year % 400 === 0) {
        daysInMonth[1] = 29;
    }

    monthContainers.forEach((container, index) => {
        container.innerHTML = ''; // Clear any previous day boxes
        for (let day = 1; day <= daysInMonth[index]; day++) {
            const dayDiv = document.createElement('div');
            dayDiv.id = `${container.parentElement.id}-${day}`;
            dayDiv.classList.add('day-box'); // Add the new class
            container.appendChild(dayDiv);
        }
    });
}



function getColorForSentiment(sentiment) {
    switch (sentiment) {
        case 'positive':
            return '#c6e48b'; // Light green
        case 'negative':
            return '#e25555'; // Light red
        case 'neutral':
            return '#7bc96f'; // Medium green
    }
}

function updateContributionGraph(tweetsData) {
    const processedData = processSentimentData(tweetsData);
    renderContributionGraph(processedData);
}


const sentimentColors = {
    admiration: "#ffc107", // gold
    amusement: "#28a745", // green
    anger: "#dc3545", // red
    annoyance: "#fd7e14", // orange
    approval: "#007bff", // blue
    caring: "#6f42c1", // purple
    confusion: "#17a2b8", // teal
    curiosity: "#e83e8c", // pink
    desire: "#6610f2", // indigo
    disappointment: "#6c757d", // gray
    disapproval: "#343a40", // dark gray
    disgust: "#20c997", // mint
    embarrassment: "#f8f9fa", // lightest gray
    excitement: "#d63384", // magenta
    fear: "#fd7e14", // dark orange
    gratitude: "#ffc107", // yellow
    grief: "#343a40", // charcoal
    joy: "#28a745", // light green
    love: "#dc3545", // dark red
    nervousness: "#17a2b8", // light blue
    optimism: "#20c997", // teal green
    pride: "#6610f2", // dark purple
    realization: "#e83e8c", // hot pink
    relief: "#6c757d", // light gray
    remorse: "#ffc107", // amber
    sadness: "#007bff", // dark blue
    surprise: "#f8f9fa", // off white
    neutral: "#6c757d" // medium gray
};


function generateBubbleWordCloud(tweets) {
    const wordFrequency = {};
    const stopwords = new Set([
        'call', 'upon', 'still', 'nevertheless', 'down', 'every', 'forty', '‘re', 'always', 'whole', 
        'side', "n't", 'now', 'however', 'an', 'show', 'least', 'give', 'below', 'did', 'sometimes', 
        'which', "'s", 'nowhere', 'per', 'hereupon', 'yours', 'she', 'moreover', 'eight', 'somewhere', 
        'within', 'whereby', 'few', 'has', 'so', 'have', 'for', 'noone', 'top', 'were', 'those', 'thence', 
        'eleven', 'after', 'no', '’ll', 'others', 'ourselves', 'themselves', 'though', 'that', 'nor', 'just', 
        '’s', 'before', 'had', 'toward', 'another', 'should', 'herself', 'and', 'these', 'such', 'elsewhere', 
        'further', 'next', 'indeed', 'bottom', 'anyone', 'his', 'each', 'then', 'both', 'became', 'third', 
        'whom', '‘ve', 'mine', 'take', 'many', 'anywhere', 'to', 'well', 'thereafter', 'besides', 'almost', 
        'front', 'fifteen', 'towards', 'none', 'be', 'herein', 'two', 'using', 'whatever', 'please', 'perhaps', 
        'full', 'ca', 'we', 'latterly', 'here', 'therefore', 'us', 'how', 'was', 'made', 'the', 'or', 'may', 
        '’re', 'namely', "'ve", 'anyway', 'amongst', 'used', 'ever', 'of', 'there', 'than', 'why', 'really', 
        'whither', 'in', 'only', 'wherein', 'last', 'under', 'own', 'therein', 'go', 'seems', '‘m', 'wherever', 
        'either', 'someone', 'up', 'doing', 'on', 'rather', 'ours', 'again', 'same', 'over', '‘s', 'latter', 
        'during', 'done', "'re", 'put', "'m", 'much', 'neither', 'among', 'seemed', 'into', 'once', 'my', 
        'otherwise', 'part', 'everywhere', 'never', 'myself', 'must', 'will', 'am', 'can', 'else', 'although', 
        'as', 'beyond', 'are', 'too', 'becomes', 'does', 'a', 'everyone', 'but', 'some', 'regarding', '‘ll', 
        'against', 'throughout', 'yourselves', 'him', "'d", 'it', 'himself', 'whether', 'move', '’m', 'hereafter', 
        're', 'while', 'whoever', 'your', 'first', 'amount', 'twelve', 'serious', 'other', 'any', 'off', 'seeming', 
        'four', 'itself', 'nothing', 'beforehand', 'make', 'out', 'very', 'already', 'various', 'until', 'hers', 
        'they', 'not', 'them', 'where', 'would', 'since', 'everything', 'at', 'together', 'yet', 'more', 'six', 
        'back', 'with', 'thereupon', 'becoming', 'around', 'due', 'keep', 'somehow', 'n‘t', 'across', 'all', 'when', 
        'i', 'empty', 'nine', 'five', 'get', 'see', 'been', 'name', 'between', 'hence', 'ten', 'several', 'from', 
        'whereupon', 'through', 'hereby', "'ll", 'alone', 'something', 'formerly', 'without', 'above', 'onto', 
        'except', 'enough', 'become', 'behind', '’d', 'its', 'most', 'n’t', 'might', 'whereas', 'anything', 'if', 
        'her', 'via', 'fifty', 'is', 'thereby', 'twenty', 'often', 'whereafter', 'their', 'also', 'anyhow', 'cannot', 
        'our', 'could', 'because', 'who', 'beside', 'by', 'whence', 'being', 'meanwhile', 'this', 'afterwards', 
        'whenever', 'mostly', 'what', 'one', 'nobody', 'seem', 'less', 'do', '‘d', 'say', 'thus', 'unless', 'along', 
        'yourself', 'former', 'thru', 'he', 'hundred', 'three', 'sixty', 'me', 'sometime', 'whose', 'you', 'quite', 
        '’ve', 'about', 'even'
    ]);
    
    // Common words to ignore

    // Process tweets to extract word frequencies and sentiments
    tweets.forEach(tweet => {
        const words = tweet.text.toLowerCase().replace(/[^\w\s]|_/g, "").split(/\s+/)
            .filter(word => !stopwords.has(word) && word.length > 1);
        words.forEach(word => {
            if (!wordFrequency[word]) {
                wordFrequency[word] = { count: 0, sentiments: {} };
            }
            wordFrequency[word].count++;
            wordFrequency[word].sentiments[tweet.sentiment.subcategory] = (wordFrequency[word].sentiments[tweet.sentiment.subcategory] || 0) + 1;
        });
    });

    // Convert frequency data to chart data
    const chartData = Object.keys(wordFrequency).map(word => {
        const data = wordFrequency[word];
        const mostCommonSentiment = Object.keys(data.sentiments)
            .reduce((a, b) => data.sentiments[a] > data.sentiments[b] ? a : b);
        return {
            x: Math.random() * 100,
            y: Math.random() * 100,
            r: Math.sqrt(data.count) * 40,
            word: word,  // Including word here for labels
            sentiment: mostCommonSentiment,
            count: data.count
        };
    }).sort((a, b) => b.r - a.r).slice(0, 5);

    if (window.bubbleWordCloudInstance) {
        window.bubbleWordCloudInstance.destroy();
    }

    // Render bubble chart
    const ctx = document.getElementById('wordCloudChart').getContext('2d');
    window.bubbleWordCloudInstance = new Chart(ctx, {
        type: 'bubble',
        data: {
            datasets: [{
                label: 'Word Frequencies',
                data: chartData,
                backgroundColor: chartData.map(d => sentimentColors[d.sentiment] || "#cccccc")
            }]
        },
        options: {
            aspectRatio: 1,
            scales: {
                y: {
                    display: false
                },
                x: {
                    display: false
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const dataPoint = context.raw;
                            // Format the tooltip to show word, sentiment, and frequency
                            return `Word: ${dataPoint.word} || Sentiment: ${dataPoint.sentiment} || Frequency: ${dataPoint.count}`;
                        }
                    }
                }
            },            
            maintainAspectRatio: true
        }
    });   
    
    console.log(document.getElementById('wordCloudChart').width);
    console.log(document.getElementById('wordCloudChart').height);
}
