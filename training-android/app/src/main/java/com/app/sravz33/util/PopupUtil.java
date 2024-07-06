package com.app.sravz33.util;

import android.app.Activity;
import android.app.Dialog;
import android.view.Window;

public class PopupUtil {

    public static Dialog showCustomPopup(Activity activity, int layout, boolean cancelable) {
        Dialog dialog = new Dialog(activity);
        dialog.requestWindowFeature(Window.FEATURE_NO_TITLE);
        dialog.setCancelable(cancelable);
        dialog.setContentView(layout);
        dialog.show();
        return dialog;
    }
}
