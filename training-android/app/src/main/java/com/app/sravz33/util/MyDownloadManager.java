package com.app.sravz33.util;

import android.app.DownloadManager;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.Uri;
import android.os.Environment;
import android.webkit.DownloadListener;
import android.webkit.URLUtil;
import android.widget.Toast;
import com.app.sravz33.Home;
import com.app.sravz33.R;

import static android.content.Context.DOWNLOAD_SERVICE;

public class MyDownloadManager implements DownloadListener {
    Home activity;
    String downloadUrl = "";
    String contentDisposition = "";
    String mimeType = "";
    private long downloadReference;

    public MyDownloadManager(Home activity) {
        this.activity = activity;
    }

    @Override
    public void onDownloadStart(String url, String userAgent, String contentDisposition, String mimetype, long contentLength) {
        LogUtil.loge("onDownloadStart: "+url);
        downloadUrl = url;
        contentDisposition = contentDisposition;
        mimeType = mimetype;
        if(PermissionUtil.checkDownloadPermission(activity)) {
            downloadFile();
        }
        else{
            PermissionUtil.getDownloadPermission(activity);
        }
    }

    public void downloadFile() {
        if(downloadUrl.isEmpty())
            return;
        Toast.makeText(activity, activity.getResources().getString(R.string.downloading), Toast.LENGTH_SHORT).show();
        DownloadManager downloadManager = (DownloadManager) activity.getSystemService(DOWNLOAD_SERVICE);
        DownloadManager.Request request = new DownloadManager.Request(Uri.parse(downloadUrl));
        String fileName = URLUtil.guessFileName(downloadUrl, contentDisposition, mimeType);
        LogUtil.loge("fileName: "+fileName);
        request.setDestinationInExternalPublicDir(Environment.DIRECTORY_DOWNLOADS, fileName);
        request.setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED);
        //request.setTitle(title);
        //request.setDescription(desc);
        request.setMimeType(mimeType);
        downloadReference = downloadManager.enqueue(request);
        IntentFilter filter = new IntentFilter(DownloadManager.ACTION_DOWNLOAD_COMPLETE);
        activity.registerReceiver(downloadReceiver, filter);
    }

    private BroadcastReceiver downloadReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            //check if the broadcast message is for our enqueued download
            long referenceId = intent.getLongExtra(DownloadManager.EXTRA_DOWNLOAD_ID, -1);
            if (referenceId == downloadReference) {
                LogUtil.loge("open file");
                IntentUtil.openDownloadedAttachment(context, referenceId);
                activity.unregisterReceiver(this);
            }
        }
    };
}
