// Tuesday, In Full — grader entrypoint.
// Copies the pre-rendered entry.png (built by draw_day.py) to the output
// directory, byte-for-byte, after validating it. Node stdlib only.
import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const MAX_BYTES = 1_048_576;
const MAX_DIM = 1024;

function fail(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

function main(): void {
  const here = dirname(fileURLToPath(import.meta.url));
  const src = join(here, "entry.png");
  if (!existsSync(src)) fail(`entry.png not found beside main.ts (${src})`);

  const data = readFileSync(src);
  if (data.length === 0 || data.length > MAX_BYTES) {
    fail(`entry.png size ${data.length} out of range (max ${MAX_BYTES})`);
  }
  const signature = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
  for (let i = 0; i < signature.length; i++) {
    if (data[i] !== signature[i]) fail("entry.png has an invalid PNG signature");
  }
  if (data.length < 24) fail("entry.png too short to contain an IHDR");
  // Bytes 8-11 are the IHDR chunk length (13) and 12-15 its type, "IHDR".
  if (data.readUInt32BE(8) !== 13 || data.toString("ascii", 12, 16) !== "IHDR") {
    fail("entry.png is missing a valid IHDR chunk");
  }
  const width = data.readUInt32BE(16);
  const height = data.readUInt32BE(20);
  if (width === 0 || height === 0) fail("entry.png has zero width or height");
  if (width > MAX_DIM || height > MAX_DIM) {
    fail(`entry.png dimensions ${width}x${height} exceed ${MAX_DIM}x${MAX_DIM}`);
  }

  const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
  mkdirSync(outDir, { recursive: true });
  const dest = join(outDir, "entry.png");
  copyFileSync(src, dest);
  if (statSync(dest).size !== data.length) fail("copied file size mismatch");
  // Byte-for-byte check: the delivered file must equal the source exactly,
  // so repeated runs always produce identical output bytes.
  if (!readFileSync(dest).equals(data)) fail("copied file differs from entry.png");
  console.log(`wrote ${dest} (${data.length} bytes, ${width}x${height})`);
}

main();
