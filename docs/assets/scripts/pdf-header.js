(function () {
  function createHeader(headerSource) {
    var header = document.createElement("div");
    var image = document.createElement("img");

    header.className = "pdf-page-header";
    header.setAttribute("aria-hidden", "true");

    image.alt = "";
    image.decoding = "sync";
    image.src = headerSource;

    header.appendChild(image);

    return header;
  }

  function toHeaderPath(reference) {
    if (!reference) {
      return null;
    }

    if (/\/assets\/images\//.test(reference)) {
      return reference.replace(/\/[^/]+(?:[?#].*)?$/, "/WCRP_RIfS_CORDEX_header.png");
    }
    if (/\/assets\/stylesheets\//.test(reference)) {
      return reference.replace(/\/assets\/stylesheets\/[^/]+(?:[?#].*)?$/, "/assets/images/document_header.png");
    }

    return null;
  }

  function resolveHeaderImage() {
    var favicon = document.querySelector('link[rel~="icon"]');
    var stylesheet = document.querySelector('link[href*="/assets/stylesheets/"]');
    var image = Array.from(document.images || []).find(function (element) {
      return /\/assets\/images\//.test(element.src || "");
    });
    var source = (favicon && favicon.href) || (stylesheet && stylesheet.href) || (image && image.src) || "";

    if (!source) {
      console.error("[mkdocs-exporter] Could not locate a site asset reference to derive the PDF header image path.");
      return null;
    }

    try {
      var headerPath = toHeaderPath(source);

      if (!headerPath) {
        console.error("[mkdocs-exporter] Found a site asset reference, but could not derive the PDF header image path.");
        return null;
      }

      return new URL(headerPath, window.location.href).toString();
    } catch (error) {
      console.error("[mkdocs-exporter] Failed to resolve the PDF header image path.", error);
      return null;
    }
  }

  function injectHeaders() {
    var headerSource = resolveHeaderImage();
    var pages = Array.from(document.querySelectorAll(".pagedjs_page"));

    if (!headerSource || !pages.length) {
      return;
    }

    pages.forEach(function (page) {
      if (page.querySelector(".pdf-page-header")) {
        return;
      }

      page.appendChild(createHeader(headerSource));
    });
  }

  function patchPagedConfig(config) {
    if (!config || config.__pdfHeaderPatched) {
      return config;
    }

    var originalAfter = config.after;

    config.after = function () {
      if (typeof originalAfter === "function") {
        originalAfter();
      }

      injectHeaders();
    };
    config.__pdfHeaderPatched = true;

    return config;
  }

  var pagedConfig = window.PagedConfig;

  Object.defineProperty(window, "PagedConfig", {
    configurable: true,
    enumerable: true,
    get: function () {
      return pagedConfig;
    },
    set: function (value) {
      pagedConfig = patchPagedConfig(value);
    }
  });

  if (pagedConfig) {
    window.PagedConfig = pagedConfig;
  }
})();