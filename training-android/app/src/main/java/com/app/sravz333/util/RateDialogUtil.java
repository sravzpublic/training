package com.app.sravz333.util;

import android.app.Dialog;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.net.Uri;
import android.view.View;
import android.widget.TextView;

import com.app.sravz333.Home;
import com.app.sravz333.R;
import com.app.sravz333.Settings;

public class RateDialogUtil {

    public static boolean shouldShow(Home activity){
        if (PrefsUtil.getAppLanuches(activity) >= Settings.RATE_DIALOG_AFTER_APP_LANUCHES) {
            if (!PrefsUtil.isNoThanksPressed(activity)) {
                if(!PrefsUtil.isRateNowPressed(activity)) {
                    return true;
                }
            }
        }
        return false;
    }

    public static void showRateDialog(final Home activity) {
        LogUtil.loge("showRateDialog");
        PrefsUtil.setAppLanuches(activity, 0); // reset
        final Dialog dialog = PopupUtil.showCustomPopup(activity, R.layout.rate_dialog, false);
        TextView rateNow = dialog.findViewById(R.id.rateNow);
        TextView noThanks = dialog.findViewById(R.id.noThanks);
        TextView maybeLater = dialog.findViewById(R.id.maybeLater);
        rateNow.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Utils.clickEffect(v);
                dialog.dismiss();
                PrefsUtil.setRateNowPressed(activity, true);
                try {
                    Uri uri = Uri.parse("market://details?id="+Settings.PLAY_STORE_LINK_ID);
                    Intent goToMarket = new Intent(Intent.ACTION_VIEW, uri);
                    activity.startActivity(goToMarket);
                }
                catch (ActivityNotFoundException e) {
                    Home.currentUrl = "http://play.google.com/store/apps/details?id="+Settings.PLAY_STORE_LINK_ID;
                    activity.loadWebPage();
                }
            }
        });
        noThanks.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Utils.clickEffect(v);
                PrefsUtil.setNoThanksPressed(activity, true);
                dialog.dismiss();
            }
        });
        maybeLater.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Utils.clickEffect(v);
                dialog.dismiss();
            }
        });
    }
}
