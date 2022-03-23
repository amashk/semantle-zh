const cache = {};
let darkModeMql = window.matchMedia('(prefers-color-scheme: dark)');
let darkMode = false;

function solveStory(guesses, puzzleNumber) {
//    if (guess_count == 0) {
//        return `I gave up on Semantle ${puzzleNumber} without even guessing once.`;
//    }

//    if (guess_count == 1) {
//        return `I got Semantle ${puzzleNumber} on my first guess!`;
//    }

    txt = '我用' + guesses.length +  '次猜测解决了语义游戏#' + puzzleNumber + '!';
    txt += '\nhttps://semantle-zh.herokuapp.com\n';
    let shareGuesses = guesses.slice();
    shareGuesses.sort(function(a, b){return b[0]-a[0]});
    shareGuesses = shareGuesses.slice(0, 6);
    let greens = 0;
    let whites = 0;
    let squares = 5;
    shareGuesses.forEach(guess => {
        [similarity, old_guess, guess_number, percentile] = guess;
        greens = Math.max(Math.floor(squares * percentile / 1000), 0);
        whites = squares - greens;
        txt += '🟩'.repeat(greens) + '⬜'.repeat(whites) + ' ';
        txt += ' ' + guess_number;
        if (greens != 0) {
            txt += ' (' + percentile + '/1000)';
        }
        txt += '\n'
    }
    );

    return txt;
}


        function share() {
    // We use the stored guesses here, because those are not updated again
    // once you win -- we don't want to include post-win guesses here.
    const text = solveStory(JSON.parse(window.localStorage.getItem("guesses")), puzzleNumber.innerText);
    const copied = ClipboardJS.copy(text);

    if (copied) {
        alert("复制了，现在粘贴在社交媒体上!");
    }
    else {
        alert("无法复制到剪贴板");
    }
}

let Semantle = (function() {
    'use strict';

    let guessed = new Set();
    let firstGuess = true;
    let guesses = [];
    let guessCount = 0;
    let gameOver = false;
    const handleStats = false;
    const storage = window.localStorage;

//    TODO: use value sent from BE ?
    const now = Date.now();
    const today = Math.floor(now / 86400000);
    const initialDay = 19044;
    const puzzleNumber = today + 1 - initialDay;

    async function getSim(word) {
        if (cache.hasOwnProperty(word)) {
            return cache[word];
        }
        const url = "/api/distance" + '?word=' + word;
        const response = await fetch(url);
        try {
            return await response.json();
        } catch (e) {
            return null;
        }
    }

    function guessRow(similarity, oldGuess, percentile, guessNumber, guess) {
    let percentileText = "(远)";
    let progress = "";
    let cls = "";
    if (percentile > 0) {
        if (percentile == 1000) {
            percentileText = "找到了!";
        } else {
            cls = "close";
            percentileText = `<span style="text-align:right; width:5em; display:inline-block;">${percentile}/1000</span>&nbsp;`;
            progress = ` <span class="progress-container">
<span class="progress-bar" style="width:${percentile/10}%">&nbsp;</span>
</span>`;
        }
    }
    let color;
    if (oldGuess === guess) {
        color = '#c0c';
    } else if (darkMode) {
        color = '#fafafa';
    } else {
        color = '#000';
    }
    return `<tr><td>${guessNumber}</td>
    <td style="color:${color}" onclick="select('${oldGuess}', secretVec);">${oldGuess}</td>
    <td>${similarity.toFixed(2)}</td>
    <td class="${cls}">${percentileText}${progress}
</td></tr>`;

}

    function checkMedia() {
        const storagePrefersDarkColorScheme = storage.getItem("prefersDarkColorScheme");
        if (storagePrefersDarkColorScheme === 'true' || storagePrefersDarkColorScheme === 'false') {
            darkMode = storagePrefersDarkColorScheme === 'true';
        } else {
            darkMode = darkModeMql.matches;
            darkModeMql.onchange = (e) => {
                darkMode = e.matches;
                toggleDarkMode(darkMode)
                updateGuesses();
            }
        }
        toggleDarkMode(darkMode);
    }

    function saveGame(guessCount, winState) {
        // If we are in a tab still open from yesterday, we're done here.
        // Don't save anything because we may overwrite today's game!
        let savedPuzzleNumber = storage.getItem("puzzleNumber");
        if (savedPuzzleNumber != puzzleNumber) { return }

        storage.setItem("winState", winState);
        storage.setItem("guesses", JSON.stringify(guesses));

    };

            if (!storage.getItem("readRules")) {
            openRules();
        }

        $("#rules-button")[0].addEventListener('click', openRules);
        $("#settings-button")[0].addEventListener('click', openSettings);

        [$("#rules-underlay"), $("#rules-close")].forEach((el) => {
            el[0].addEventListener('click', () => {
                document.body.classList.remove('rules-open');
            });
        });

        $("#rules")[0].addEventListener("click", (event) => {
            // prevents click from propagating to the underlay, which closes the rules
            event.stopPropagation();
        });

    function openRules() {
        document.body.classList.add('rules-open');
        storage.setItem("readRules", true);
    }
    function openSettings() {
        document.body.classList.add('dialog-open', 'settings-open');
        $("#settings-close")[0].focus();
    }

    function updateGuesses(guess) {
        let inner = `<tr>
        <th>#</th>
        <th>猜想</th>
        <th>接近</th>
        <th>逐渐回暖?</th></tr>`;
        /* This is dumb: first we find the most-recent word, and put
           it at the top.  Then we do the rest. */
        for (let entry of guesses) {
            let [similarity, oldGuess, guessNumber, percentile] = entry;
            if (oldGuess == guess) {
                inner += guessRow(similarity, oldGuess, percentile, guessNumber, guess);
            }
        }
        inner += "<tr><td colspan=4><hr></td></tr>";
        for (let entry of guesses) {
            let [similarity, oldGuess, guessNumber, percentile] = entry;
            if (oldGuess != guess) {
                inner += guessRow(similarity, oldGuess, percentile, guessNumber);
            }
        }
        $('#guesses')[0].innerHTML = inner;
    }

    function toggleDarkMode(on) {
        document.body.classList[on ? 'add' : 'remove']('dark');
        const darkModeCheckbox = $("#dark-mode")[0];
        // this runs before the DOM is ready, so we need to check
        if (darkModeCheckbox) {
            darkModeCheckbox.checked = on;
        }
    }


    document.querySelectorAll(".dialog-underlay, .dialog-close, #capitalized-link").forEach((el) => {
            el.addEventListener('click', () => {
                document.body.classList.remove('dialog-open', 'rules-open', 'settings-open');
            });
        });

    document.querySelectorAll(".dialog").forEach((el) => {
            el.addEventListener("click", (event) => {
                // prevents click from propagating to the underlay, which closes the rules
                event.stopPropagation();
            });
        });

    $("#dark-mode")[0].addEventListener('click', function(event) {
        storage.setItem("prefersDarkColorScheme", event.target.checked);
        darkModeMql.onchange = null;
        darkMode = event.target.checked;
        toggleDarkMode(darkMode);
        updateGuesses();
    });

    toggleDarkMode(darkMode);

    if (storage.getItem("prefersDarkColorScheme") === null) {
        $("#dark-mode")[0].checked = false;
        $("#dark-mode")[0].indeterminate = true;
    }

    async function init() {
    $('#form')[0].addEventListener('submit', async function(event) {
            event.preventDefault();
            $('#guess').focus();
            $('#error')[0].textContent = "";
            let guess = $('#guess')[0].value.trim().replace("!", "").replace("*", "");
            if (!guess) {
                return false;
            }

            $('#guess')[0].value = "";

            const guessData = await getSim(guess);
            if (guessData.similarity < 0) {
                $('#error')[0].textContent = `我不知道${guess}是什么.`;
                return false;
            }

            let score = guessData.similarity;

            const distance = guessData.distance;

            cache[guess] = guessData;

            let similarity = guessData.similarity;
            if (!guessed.has(guess)) {
                guessCount += 1;
                guessed.add(guess);

                const newEntry = [similarity, guess, guessCount, distance];
                guesses.push(newEntry);
                if (distance == 1000){
                    endGame(true, true);
                }
            }
            guesses.sort(function(a, b){return b[0]-a[0]});
            if (!gameOver){
                saveGame(-1, -1);
            }


            updateGuesses(guess);

            firstGuess = false;
//            if (guess.toLowerCase() === secret && !gameOver) {
//                endGame(guesses.length);
//            }
            return false;
        });

//        let puzzleNumber = $("#puzzleNumber")[0].innerText;
        let storagePuzzleNumber = storage.getItem("puzzleNumber");
        if (storagePuzzleNumber != puzzleNumber) {
            storage.removeItem("guesses");
            storage.removeItem("winState");
            storage.setItem("puzzleNumber", puzzleNumber);
        }

        const winState = storage.getItem("winState");
        if (winState != null) {
            guesses = JSON.parse(storage.getItem("guesses"));
            guesses.sort(function(a, b){return b[0]-a[0]});
            for (let guess of guesses) {
                guessed.add(guess[1]);
            }
            guessCount = guessed.size;
            updateGuesses("");
            if (winState != -1) {
                endGame(winState);
            }
        }
        }

        function endGame(won, countStats) {
        let stats;
        if (handleStats) {
            stats = getStats();
            if (countStats) {
                const onStreak = (stats['lastEnd'] == puzzleNumber - 1);

                stats['lastEnd'] = puzzleNumber;
                if (won) {
                    if (onStreak) {
                        stats['winStreak'] += 1;
                    } else {
                    stats['winStreak'] = 1;
                    }
                    stats['wins'] += 1;
                } else {
                    stats['winStreak'] = 0;
                    stats['giveups'] += 1;
                }
                storage.setItem("stats", JSON.stringify(stats));
            }
        }

        gameOver = true;
        let response;
        if (won) {
            response = `<p><b>
            你赢了！
            你在${guesses.length}次猜测中找到了解决方案！
            您可以继续输入单词并查看它们的接近度，
            还有 <a href="javascript:share();">分享</a>
            明天回来在玩儿。
             </p>`
        } else {
        // right now we do not allow giving up
            response = `<p><b>You gave up!  The secret word is: ${secret}</b>.  Feel free to keep entering words if you are curious about the similarity to other words.  You can see the nearest words <a href="nearby_1k/${secretBase64}">here</a>.</p>`;
        }

        if (handleStats) {
            const totalGames = stats['wins'] + stats['giveups'] + stats['abandons'];
            response += `<br/>
Stats (since we started recording, on day 23): <br/>
<table>
<tr><th>First game:</th><td>${stats['firstPlay']}</td></tr>
<tr><th>Total days played:</th><td>${totalGames}</td></tr>
<tr><th>Wins:</th><td>${stats['wins']}</td></tr>
<tr><th>Win streak:</th><td>${stats['winStreak']}</td></tr>
<tr><th>Give-ups:</th><td>${stats['giveups']}</td></tr>
<tr><th>Did not finish</th><td>${stats['abandons']}</td></tr>
<tr><th>Total guesses across all games:</th><td>${stats['totalGuesses']}</td></tr>
</table>
`;
        }
        $('#response')[0].innerHTML = response;

        if (endGame) {
            saveGame(guesses.length, won ? 1 : 0);
        }
    }

        return {
        init: init,
        checkMedia: checkMedia
    };
})();

// do this when the file loads instead of waiting for DOM to be ready to avoid
// a flash of unstyled content
Semantle.checkMedia();

window.addEventListener('load', async () => { Semantle.init() });