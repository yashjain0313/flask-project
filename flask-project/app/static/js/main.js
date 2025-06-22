// Task Manager JavaScript

document.addEventListener("DOMContentLoaded", function () {
  // Initialize tooltips
  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Auto-hide alerts after 5 seconds
  setTimeout(function () {
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach(function (alert) {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    });
  }, 5000);

  // Add confirmation for delete buttons
  const deleteButtons = document.querySelectorAll(".btn-delete");
  deleteButtons.forEach(function (button) {
    button.addEventListener("click", function (e) {
      if (!confirm("Are you sure you want to delete this task?")) {
        e.preventDefault();
      }
    });
  });

  // Add loading state to form submissions
  const forms = document.querySelectorAll("form");
  forms.forEach(function (form) {
    form.addEventListener("submit", function () {
      const submitButton = form.querySelector('button[type="submit"]');
      if (submitButton) {
        submitButton.disabled = true;
        submitButton.innerHTML =
          '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Loading...';
      }
    });
  });

  // Task completion animation
  const taskCards = document.querySelectorAll(".task-card");
  taskCards.forEach(function (card) {
    card.classList.add("fade-in");
  });

  // Filter form auto-submit
  const filterSelects = document.querySelectorAll(
    'select[name="category"], select[name="status"]'
  );
  filterSelects.forEach(function (select) {
    select.addEventListener("change", function () {
      // Optional: Auto-submit filter form when selection changes
      // Uncomment the line below if you want automatic filtering
      // this.form.submit();
    });
  });

  // Character counter for task description
  const descriptionTextarea = document.querySelector(
    'textarea[name="description"]'
  );
  if (descriptionTextarea) {
    const maxLength = 500;
    const counter = document.createElement("small");
    counter.className = "text-muted";
    counter.textContent = `0/${maxLength} characters`;
    descriptionTextarea.parentNode.appendChild(counter);

    descriptionTextarea.addEventListener("input", function () {
      const currentLength = this.value.length;
      counter.textContent = `${currentLength}/${maxLength} characters`;

      if (currentLength > maxLength * 0.9) {
        counter.className = "text-warning";
      } else if (currentLength === maxLength) {
        counter.className = "text-danger";
      } else {
        counter.className = "text-muted";
      }
    });
  }

  // Add smooth scrolling for anchor links
  const anchorLinks = document.querySelectorAll('a[href^="#"]');
  anchorLinks.forEach(function (link) {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });

  // Task priority color coding
  function updatePriorityColors() {
    const priorityElements = document.querySelectorAll("[data-priority]");
    priorityElements.forEach(function (element) {
      const priority = element.dataset.priority.toLowerCase();
      element.classList.remove(
        "priority-urgent",
        "priority-high",
        "priority-medium",
        "priority-low"
      );
      element.classList.add("priority-" + priority);
    });
  }

  updatePriorityColors();

  // Keyboard shortcuts
  document.addEventListener("keydown", function (e) {
    // Ctrl/Cmd + N for new task
    if ((e.ctrlKey || e.metaKey) && e.key === "n") {
      e.preventDefault();
      const newTaskLink = document.querySelector('a[href*="new_task"]');
      if (newTaskLink) {
        window.location.href = newTaskLink.href;
      }
    }

    // Escape key to close modals
    if (e.key === "Escape") {
      const openModals = document.querySelectorAll(".modal.show");
      openModals.forEach(function (modal) {
        const bsModal = bootstrap.Modal.getInstance(modal);
        if (bsModal) {
          bsModal.hide();
        }
      });
    }
  });

  // Task search functionality (if search input exists)
  const searchInput = document.querySelector("#taskSearch");
  if (searchInput) {
    searchInput.addEventListener("input", function () {
      const searchTerm = this.value.toLowerCase();
      const taskCards = document.querySelectorAll(".task-card");

      taskCards.forEach(function (card) {
        const title = card
          .querySelector(".card-title")
          .textContent.toLowerCase();
        const description = card.querySelector(".card-text");
        const descText = description
          ? description.textContent.toLowerCase()
          : "";

        if (title.includes(searchTerm) || descText.includes(searchTerm)) {
          card.style.display = "block";
          card.parentElement.style.display = "block";
        } else {
          card.style.display = "none";
          card.parentElement.style.display = "none";
        }
      });
    });
  }

  // Add visual feedback for successful actions
  function showSuccessMessage(message) {
    const alertDiv = document.createElement("div");
    alertDiv.className =
      "alert alert-success alert-dismissible fade show position-fixed";
    alertDiv.style.top = "20px";
    alertDiv.style.right = "20px";
    alertDiv.style.zIndex = "9999";
    alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
    document.body.appendChild(alertDiv);

    setTimeout(function () {
      alertDiv.remove();
    }, 3000);
  }

  // Handle AJAX form submissions (if needed in the future)
  function handleAjaxForm(form, successCallback) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();

      const formData = new FormData(form);
      const submitButton = form.querySelector('button[type="submit"]');

      // Show loading state
      if (submitButton) {
        submitButton.disabled = true;
        submitButton.innerHTML =
          '<span class="spinner-border spinner-border-sm me-2"></span>Saving...';
      }

      fetch(form.action, {
        method: "POST",
        body: formData,
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            if (successCallback) {
              successCallback(data);
            }
            showSuccessMessage(
              data.message || "Operation completed successfully!"
            );
          } else {
            throw new Error(data.message || "Operation failed");
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          showErrorMessage(error.message || "An error occurred");
        })
        .finally(() => {
          // Restore button state
          if (submitButton) {
            submitButton.disabled = false;
            submitButton.innerHTML =
              submitButton.dataset.originalText || "Submit";
          }
        });
    });
  }

  // Show error message
  function showErrorMessage(message) {
    const alertDiv = document.createElement("div");
    alertDiv.className =
      "alert alert-danger alert-dismissible fade show position-fixed";
    alertDiv.style.top = "20px";
    alertDiv.style.right = "20px";
    alertDiv.style.zIndex = "9999";
    alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
    document.body.appendChild(alertDiv);

    setTimeout(function () {
      alertDiv.remove();
    }, 5000);
  }
});
