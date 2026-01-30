# Deploying RoomFinder on Render (images with Cloudinary)

## 1. Set Cloudinary environment variables on Render

In **Render Dashboard** → your **Web Service** → **Environment**:

**Option A – three variables** (get values from [Cloudinary Console](https://cloudinary.com/console)):

| Key                     | Value              |
|-------------------------|--------------------|
| `CLOUDINARY_CLOUD_NAME` | Your cloud name    |
| `CLOUDINARY_API_KEY`    | Your API key       |
| `CLOUDINARY_API_SECRET` | Your API secret    |

**Option B – single variable:**

| Key              | Value                                      |
|------------------|--------------------------------------------|
| `CLOUDINARY_URL` | `cloudinary://API_KEY:API_SECRET@CLOUD_NAME` |

If Cloudinary is not configured, the app will fail to start on Render with a clear error.

## 2. Existing rooms created locally

Rooms you created **before** deploying use image paths that point to files that only exist in your local `media/` folder. Those files were **not** uploaded to Cloudinary, so on Render those image URLs will 404.

**Fix:** On your live site, open each listing → **Edit Listing** → re-upload the cover image (and gallery images if any). Save. New uploads go to Cloudinary and will display correctly.

New rooms created **on Render** (after env vars are set) will have their images stored on Cloudinary and will show correctly.

## 3. After redeploy

Redeploy the service after adding the env vars. New uploads will be stored on Cloudinary and images will show. Re-upload cover/gallery images for any listings that were created locally (see step 2).
