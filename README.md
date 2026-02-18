# 👁️ beady-eye

**displayio in JavaScript** - A JavaScript library that brings CircuitPython's displayio API to web browsers.

## What is beady-eye?

beady-eye is a JavaScript implementation of the displayio library (from CircuitPython), enabling developers to create visual displays in web browsers using familiar displayio patterns and APIs. Perfect for:
- Creating web-based simulations of embedded displays
- Rapid prototyping of display layouts
- Educational tools for learning displayio
- Cross-platform display development

## Current Status

🚧 **Early Development / Proof of Concept** 🚧

The project currently demonstrates basic canvas rendering with rectangles and a group system. See [MVP_PLAN.md](MVP_PLAN.md) for the complete roadmap.

## Quick Start

Open `index.html` in a web browser to see the current demo.

```html
<!DOCTYPE html>
<html>
<body>
    <canvas id="display" width="320" height="240"></canvas>
    <script src="beady-eye.js"></script>
    <script>
        // Create display
        let canvas = document.getElementById("display");
        let display = beadyeye.Display({ canvas: canvas });
        
        // Create shapes
        let group = beadyeye.Group();
        let rect = beadyeye.shapes.Rect({
            x: 10, y: 10,
            width: 100, height: 50,
            fill: 'blue'
        });
        
        group.append(rect);
        display.show(group);
    </script>
</body>
</html>
```

## Features (Planned for MVP)

### Core Features
- ✅ Display management
- ✅ Basic shapes (Rectangle)
- ⏳ Additional shapes (Circle, Line, Polygon)
- ⏳ Text rendering
- ⏳ Color management
- ⏳ Group/layer system
- ⏳ Bitmap support
- ⏳ Event handling

### API Design
The API is designed to be familiar to displayio users while leveraging JavaScript features:

```javascript
// Shapes
const rect = beadyeye.shapes.Rect({ x: 0, y: 0, width: 100, height: 50, fill: 'red' });
const circle = beadyeye.shapes.Circle({ x: 50, y: 50, radius: 20, fill: 'blue' });

// Text
const label = beadyeye.text.Label({ text: "Hello", x: 10, y: 10, color: 'white' });

// Groups
const group = beadyeye.Group();
group.append(rect);
group.append(circle);

// Display
display.show(group);
display.refresh();
```

## Documentation

- [MVP Plan](MVP_PLAN.md) - Complete MVP roadmap and feature list
- API Documentation - Coming soon
- Examples - Coming soon

## Development

### Project Structure
```
beady-eye/
├── src/              # Source code (coming soon)
├── examples/         # Example files (coming soon)
├── docs/            # Documentation (coming soon)
├── index.html       # Current demo
├── site.css         # Styles
└── MVP_PLAN.md      # Development roadmap
```

### Contributing

This project is in early development. Contributions are welcome! Please check the [MVP_PLAN.md](MVP_PLAN.md) for planned features and priorities.

## Inspiration

This project is inspired by [CircuitPython's displayio](https://docs.circuitpython.org/en/latest/shared-bindings/displayio/index.html), which provides a high-level API for driving displays on microcontrollers.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Author

Randall Bohn

## Resources

- [CircuitPython displayio Documentation](https://docs.circuitpython.org/en/latest/shared-bindings/displayio/index.html)
- [HTML5 Canvas API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API)

---

**Status**: Alpha / Proof of Concept  
**Version**: 0.1.0-alpha  
**Last Updated**: February 2026
