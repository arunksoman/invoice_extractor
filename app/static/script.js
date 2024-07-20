const $ = document.querySelector.bind(document);

/**
 * Collection of rectangles defining user generated regions
 */
const rectangles = [];

// DOM elements
const $pdf_image = $("#pdf-image");
const $draw = $("#draw");
const $rect_box = $("#rect-box");
const $boxes = $("#boxes");

// Temp variables
let startX = 0;
let startY = 0;
const marqueeRect = {
  x: 0,
  y: 0,
  width: 0,
  height: 0,
};

$rect_box.classList.add("hide");
$pdf_image.addEventListener("pointerdown", startDrag);

function startDrag(ev) {
  // middle button delete rect
  if (ev.button === 1) {
    const rect = hitTest(ev.layerX, ev.layerY);
    if (rect) {
      rectangles.splice(rectangles.indexOf(rect), 1);
      redraw();
    }
    return;
  }
  window.addEventListener("pointerup", stopDrag);
  $pdf_image.addEventListener("pointermove", moveDrag);
  $rect_box.classList.remove("hide");
  startX = ev.layerX;
  startY = ev.layerY;
  drawRect($rect_box, startX, startY, 0, 0);
}

function stopDrag(ev) {
  $rect_box.classList.add("hide");
  window.removeEventListener("pointerup", stopDrag);
  $pdf_image.removeEventListener("pointermove", moveDrag);
  if (ev.target === $pdf_image && marqueeRect.width && marqueeRect.height) {
    rectangles.push(Object.assign({}, marqueeRect));
    redraw();
  }
}

function moveDrag(ev) {
  let x = ev.layerX;
  let y = ev.layerY;
  let width = startX - x;
  let height = startY - y;
  if (width < 0) {
    width *= -1;
    x -= width;
  }
  if (height < 0) {
    height *= -1;
    y -= height;
  }
  Object.assign(marqueeRect, { x, y, width, height });
  drawRect($rect_box, marqueeRect);
}

function hitTest(x, y) {
  return rectangles.find(
    (rect) =>
      x >= rect.x &&
      y >= rect.y &&
      x <= rect.x + rect.width &&
      y <= rect.y + rect.height
  );
}

function redraw() {
  boxes.innerHTML = "";
  rectangles.forEach((data) => {
    boxes.appendChild(
      drawRect(
        document.createElementNS("http://www.w3.org/2000/svg", "rect"),
        data
      )
    );
  });
}

function drawRect(rect, data) {
  const { x, y, width, height } = data;
  rect.setAttributeNS(null, "width", width);
  rect.setAttributeNS(null, "height", height);
  rect.setAttributeNS(null, "x", x);
  rect.setAttributeNS(null, "y", y);
  return rect;
}
