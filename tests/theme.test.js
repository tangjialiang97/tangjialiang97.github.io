/**
 * Tests for the theme-related functions in assets/js/_main.js
 *
 * The functions under test (determineThemeSetting, determineComputedTheme,
 * setTheme, toggleTheme) rely on localStorage, jQuery, and window.matchMedia.
 * We mock those dependencies here so we can test the logic in isolation.
 */

// ---------------------------------------------------------------------------
// Mocks
// ---------------------------------------------------------------------------

let mockStorage = {};

const localStorageMock = {
  getItem: (key) => mockStorage[key] ?? null,
  setItem: (key, value) => { mockStorage[key] = String(value); },
  removeItem: (key) => { delete mockStorage[key]; },
  clear: () => { mockStorage = {}; },
};

Object.defineProperty(global, 'localStorage', { value: localStorageMock });

// Minimal jQuery mock
let htmlAttrs = {};
let iconClasses = new Set(["fa-sun"]);

const jQueryMock = (selector) => {
  if (selector === "html") {
    return {
      attr: (name, value) => {
        if (value === undefined) return htmlAttrs[name];
        htmlAttrs[name] = value;
        return jQueryMock(selector);
      },
      removeAttr: (name) => { delete htmlAttrs[name]; },
    };
  }
  if (selector === "#theme-icon") {
    return {
      removeClass: (cls) => {
        iconClasses.delete(cls);
        return jQueryMock(selector);
      },
      addClass: (cls) => {
        iconClasses.add(cls);
        return jQueryMock(selector);
      },
    };
  }
  return { on: () => {} };
};
global.$ = jQueryMock;

// matchMedia mock
let prefersLight = true;
global.window = global.window || {};
global.window.matchMedia = (query) => ({
  matches: query === "(prefers-color-scheme: dark)" ? !prefersLight : prefersLight,
});

// ---------------------------------------------------------------------------
// Re-implement the functions under test (extracted from _main.js)
// We cannot directly import _main.js because it has jQuery/DOM side effects.
// ---------------------------------------------------------------------------

function determineThemeSetting() {
  let themeSetting = localStorage.getItem("theme");
  return (themeSetting !== "dark" && themeSetting !== "light" && themeSetting !== "system")
    ? "system"
    : themeSetting;
}

function determineComputedTheme() {
  let themeSetting = determineThemeSetting();
  if (themeSetting !== "system") {
    return themeSetting;
  }
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

function setTheme(theme) {
  const browserPref = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  const use_theme = theme || localStorage.getItem("theme") || $("html").attr("data-theme") || browserPref;

  if (use_theme === "dark") {
    $("html").attr("data-theme", "dark");
    $("#theme-icon").removeClass("fa-sun").addClass("fa-moon");
  } else if (use_theme === "light") {
    $("html").removeAttr("data-theme");
    $("#theme-icon").removeClass("fa-moon").addClass("fa-sun");
  }
}

function toggleTheme() {
  const current_theme = $("html").attr("data-theme");
  const new_theme = current_theme === "dark" ? "light" : "dark";
  localStorage.setItem("theme", new_theme);
  setTheme(new_theme);
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

beforeEach(() => {
  localStorageMock.clear();
  htmlAttrs = {};
  iconClasses = new Set(["fa-sun"]);
  prefersLight = true;
});

describe("determineThemeSetting", () => {
  test("returns 'system' when localStorage has no theme", () => {
    expect(determineThemeSetting()).toBe("system");
  });

  test("returns 'dark' when localStorage theme is 'dark'", () => {
    localStorage.setItem("theme", "dark");
    expect(determineThemeSetting()).toBe("dark");
  });

  test("returns 'light' when localStorage theme is 'light'", () => {
    localStorage.setItem("theme", "light");
    expect(determineThemeSetting()).toBe("light");
  });

  test("returns 'system' when localStorage theme is 'system'", () => {
    localStorage.setItem("theme", "system");
    expect(determineThemeSetting()).toBe("system");
  });

  test("returns 'system' for invalid/unknown theme values", () => {
    localStorage.setItem("theme", "blue");
    expect(determineThemeSetting()).toBe("system");
  });
});

describe("determineComputedTheme", () => {
  test("returns 'dark' when theme setting is 'dark'", () => {
    localStorage.setItem("theme", "dark");
    expect(determineComputedTheme()).toBe("dark");
  });

  test("returns 'light' when theme setting is 'light'", () => {
    localStorage.setItem("theme", "light");
    expect(determineComputedTheme()).toBe("light");
  });

  test("returns 'light' when system and OS prefers light", () => {
    prefersLight = true;
    expect(determineComputedTheme()).toBe("light");
  });

  test("returns 'dark' when system and OS prefers dark", () => {
    prefersLight = false;
    expect(determineComputedTheme()).toBe("dark");
  });
});

describe("setTheme", () => {
  test("sets dark theme correctly", () => {
    setTheme("dark");
    expect(htmlAttrs["data-theme"]).toBe("dark");
    expect(iconClasses.has("fa-moon")).toBe(true);
    expect(iconClasses.has("fa-sun")).toBe(false);
  });

  test("sets light theme correctly", () => {
    htmlAttrs["data-theme"] = "dark";
    setTheme("light");
    expect(htmlAttrs["data-theme"]).toBeUndefined();
    expect(iconClasses.has("fa-sun")).toBe(true);
    expect(iconClasses.has("fa-moon")).toBe(false);
  });

  test("falls back to localStorage when no argument", () => {
    localStorage.setItem("theme", "dark");
    setTheme();
    expect(htmlAttrs["data-theme"]).toBe("dark");
  });

  test("falls back to browser pref when nothing else set", () => {
    prefersLight = true;
    setTheme();
    // light → removes data-theme
    expect(htmlAttrs["data-theme"]).toBeUndefined();
  });
});

describe("toggleTheme", () => {
  test("toggles from dark to light", () => {
    htmlAttrs["data-theme"] = "dark";
    toggleTheme();
    expect(localStorage.getItem("theme")).toBe("light");
    expect(htmlAttrs["data-theme"]).toBeUndefined();
  });

  test("toggles from light (no data-theme) to dark", () => {
    // no data-theme attr means light
    toggleTheme();
    expect(localStorage.getItem("theme")).toBe("dark");
    expect(htmlAttrs["data-theme"]).toBe("dark");
  });
});
