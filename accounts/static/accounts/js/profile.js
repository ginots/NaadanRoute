
  document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.querySelector('#profile-dashboard .sidebar');
    const toggleBtn = document.querySelector('.sidebar-toggle');

    if (toggleBtn && sidebar) {
      toggleBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        sidebar.classList.toggle('is-open');
      });
    }

    // Close sidebar when clicking anywhere outside of it
    document.addEventListener('click', function(e) {
      if (sidebar.classList.contains('is-open')) {
        if (!sidebar.contains(e.target) && e.target !== toggleBtn) {
          sidebar.classList.remove('is-open');
        }
      }
    });

    // Close sidebar if a link inside it is clicked (good for mobile)
    const navLinks = sidebar.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        sidebar.classList.remove('is-open');
      });
    });
  });




// --- Calendar generation ---
const calendarBody = document.getElementById("calendarBody");
const calendarTitle = document.getElementById("calendarTitle");
const prevBtn = document.getElementById("prevMonth");
const nextBtn = document.getElementById("nextMonth");
const todayBtn = document.getElementById("todayBtn");

let current = new Date();
current.setDate(1);

function formatMonthYear(d) {
  return d.toLocaleDateString(undefined, { month: "long", year: "numeric" });
}

const festivalData = {
                              "01-01": "New Year's Day",
                              "01-14": "Makaravilakku",
                              "02-23": "Chettikulangara Bharani",
                              "03-01": "Kochi Muziris Biennale (ongoing)",
                              "04-14": "Vishu Festival",
                              "08-15": "Independence Day",
                              "09-05": "Onam Celebration",
                              "11-01": "Kerala Piravi",
                            };

function buildCalendar(baseDate) {
  // Base month
  const year = baseDate.getFullYear();
  const month = baseDate.getMonth();
  const firstDayIndex = (new Date(year, month, 1).getDay() + 6) % 7; // Mon=0
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  // Previous month padding
  const prevDays = new Date(year, month, 0).getDate();

  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const cells = [];

  // Leading days
  for (let i = firstDayIndex; i > 0; i--) {
    const d = new Date(year, month - 1, prevDays - i + 1);
    cells.push({ d, other: true });
  }
  // Current month
  for (let i = 1; i <= daysInMonth; i++) {
    const d = new Date(year, month, i);
    cells.push({ d, other: false });
  }
  // Trailing days to complete 42 cells (6 weeks)
  while (cells.length % 7 !== 0 || cells.length < 42) {
    const last = cells[cells.length - 1].d;
    const d = new Date(last.getFullYear(), last.getMonth(), last.getDate() + 1);
    cells.push({ d, other: true });
  }

calendarBody.innerHTML = cells
  .map(({ d, other }) => {
    const isToday = d.getTime() === today.getTime();

    // 1. Formatting current date as MM-DD to match festival list
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const date = String(d.getDate()).padStart(2, '0');
    const dateKey = `${month}-${date}`;

    // 2. Look up the festival name (only if it's not an "other" month day)
    const festivalName = !other ? festivalData[dateKey] : "";

    return `
      <div class="day ${other ? "other" : ""} ${isToday ? "today" : ""}"
           role="gridcell"
           aria-selected="${isToday}">
        <div class="date">${d.getDate()}</div>
        ${festivalName ? `<span class="badge festival-badge">${festivalName}</span>` : ""}
      </div>
    `;
  })
  .join("");

  calendarTitle.textContent = `Cultural Compass – ${formatMonthYear(baseDate)}`;
}

buildCalendar(current);
prevBtn.addEventListener("click", () => {
  current.setMonth(current.getMonth() - 1);
  buildCalendar(current);
});
nextBtn.addEventListener("click", () => {
  current.setMonth(current.getMonth() + 1);
  buildCalendar(current);
});
todayBtn.addEventListener("click", () => {
  current = new Date();
  current.setDate(1);
  buildCalendar(current);
});


