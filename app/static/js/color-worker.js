self.onmessage = (event) => {
    const pixels = event.data.data;
    const colorBuckets = {};
    const step = 40; // sample every 10th pixel

    for (let i = 0; i < pixels.length; i += step) {
        const r = pixels[i];
        const g = pixels[i + 1];
        const b = pixels[i + 2];

        // Quantize to reduce unique colors (to 24 buckets per channel)
        const key = `${r >> 4}-${g >> 4}-${b >> 4}`;
        colorBuckets[key] = (colorBuckets[key] || 0) + 1;
    }

    // Find most frequent bucket
    let dominantKey = null,
        maxCount = 0;
    for (const [key, count] of Object.entries(colorBuckets)) {
        if (count > maxCount) {
            maxCount = count;
            dominantKey = key;
        }
    }

    const [rQ, gQ, bQ] = dominantKey.split("-").map((n) => parseInt(n, 10));
    const color = [rQ << 4, gQ << 4, bQ << 4];

    self.postMessage(color);
};
