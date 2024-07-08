package com.app.sravz333.util;

import android.content.Intent;
import android.os.Environment;
import android.os.Parcelable;
import android.provider.MediaStore;
import androidx.core.content.FileProvider;
import com.app.sravz333.Home;
import com.app.sravz333.R;
import java.io.File;
import java.io.IOException;

public class FilePicker {

    public static void openChooser(Home activity) {
        if(PermissionUtil.checkCameraPermission(activity)) {
            if (PermissionUtil.checkWritePermission(activity)) {
                setImageUri(activity);
                final Intent photoIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                photoIntent.putExtra(MediaStore.EXTRA_OUTPUT, Home.mPhotoCapturedURI);
                Intent i = new Intent(Intent.ACTION_GET_CONTENT);
                i.addCategory(Intent.CATEGORY_OPENABLE);
                i.setType("*/*");
                // Create file chooser intent
                Intent chooserIntent = Intent.createChooser(i, activity.getString(R.string.source));
                // Set camera intent to file chooser
                chooserIntent.putExtra(Intent.EXTRA_INITIAL_INTENTS, new Parcelable[]{photoIntent});
                // On select image call onActivityResult method of activity
                activity.startActivityForResult(chooserIntent, Home.FILECHOOSER_RESULTCODE);
            }
            else{
                PermissionUtil.getWritePermission(activity);
            }
        }
        else{
            PermissionUtil.getCameraPermission(activity);
        }
    }

    private static void setImageUri(Home activity){
        File folder = activity.getExternalFilesDir(Environment.DIRECTORY_DCIM);
        folder.mkdirs();
        File file = new File(folder, "IMG_" + System.currentTimeMillis() + ".jpg");
        try {
            boolean created = file.createNewFile();
            if(created){
                Home.mPhotoCapturedURI = FileProvider.getUriForFile(
                        activity,
                        "com.app.sravz333.fileprovider",
                        file
                );
                LogUtil.loge("fileUri: "+Home.mPhotoCapturedURI.toString());
                LogUtil.loge("filePath: "+file.getAbsolutePath());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
