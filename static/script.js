// DELETE CONFIRMATION
function confirmDelete() {

    return confirm("Are you sure you want to delete this task?");

}

// WELCOME MESSAGE
window.onload = function () {

    setTimeout(() => {

        alert("Welcome to Task Manager 🚀");

    }, 500);

};

// TASK SEARCH
function searchTasks() {

    let input = document.getElementById("searchInput").value.toLowerCase();

    let tasks = document.getElementsByClassName("task-card");

    for (let i = 0; i < tasks.length; i++) {

        let taskText = tasks[i].innerText.toLowerCase();

        if (taskText.includes(input)) {

            tasks[i].style.display = "block";

        } else {

            tasks[i].style.display = "none";

        }
    }
}

// DARK MODE
function toggleDarkMode() {

    document.body.classList.toggle("dark-mode");

}

// LIVE CLOCK
function updateClock() {

    let now = new Date();

    let time = now.toLocaleTimeString();

    document.getElementById("clock").innerHTML = time;

}

setInterval(updateClock, 1000);

// EMPTY TASK VALIDATION
function validateTask() {

    let task = document.getElementById("taskInput").value;

    if (task.trim() === "") {

        alert("Task cannot be empty!");

        return false;
    }

    return true;
}