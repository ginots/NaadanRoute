function initSignInModal() {
  const modal = document.getElementById("signInModal");
  if (!modal) return;

  const container = modal.querySelector("#authContainer");
  const signUpButton = modal.querySelector("#signUp");
  const signInButton = modal.querySelector("#signIn");
  const signInForm = modal.querySelector(".sign-in-container");
  const signUpForm = modal.querySelector(".sign-up-container");

  // 🔹 If you added inline mobile toggle links:
  const mobileSignUpToggle = document.getElementById("mobileSignUpToggle");
  const mobileSignInToggle = document.getElementById("mobileSignInToggle");

  function isMobile() {
    return window.innerWidth <= 768;
  }

  // Desktop overlay buttons
  if (signUpButton) {
    signUpButton.addEventListener("click", () => {
      if (isMobile()) {
        signInForm.style.display = "none";
        signUpForm.style.display = "block";
      } else {
        container.classList.add("right-panel-active");
      }
    });
  }

  if (signInButton) {
    signInButton.addEventListener("click", () => {
      if (isMobile()) {
        signUpForm.style.display = "none";
        signInForm.style.display = "block";
      } else {
        container.classList.remove("right-panel-active");
      }
    });
  }

  // 🔹 Mobile inline toggle links
  if (mobileSignUpToggle) {
    mobileSignUpToggle.addEventListener("click", (e) => {
      e.preventDefault();
      signInForm.style.display = "none";
      signUpForm.style.display = "block";
    });
  }

  if (mobileSignInToggle) {
    mobileSignInToggle.addEventListener("click", (e) => {
      e.preventDefault();
      signUpForm.style.display = "none";
      signInForm.style.display = "block";
    });
  }

  // Reset layout on resize
  window.addEventListener("resize", () => {
    if (isMobile()) {
      container.classList.remove("right-panel-active");
      signInForm.style.display = "block";
      signUpForm.style.display = "none";
    } else {
      signInForm.style.display = "";
      signUpForm.style.display = "";
    }
  });
}

document.addEventListener("DOMContentLoaded", initSignInModal);

