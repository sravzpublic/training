package com.app.sravz33.util;

import android.graphics.Color;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;
import androidx.core.view.GravityCompat;
import androidx.drawerlayout.widget.DrawerLayout;
import com.app.sravz33.Home;
import com.app.sravz33.R;
import com.app.sravz33.Settings;
import com.google.android.material.bottomnavigation.BottomNavigationView;

public class DrawerUtil {
    Home activity;
    DrawerLayout drawerLayout;
    boolean open = false;
    ViewGroup titleBar;
    ImageView menu, back, refresh;
    TextView title;

    public DrawerUtil(Home activity) {
        this.activity = activity;
    }

    public void openDrawer() {
        open = true;
        drawerLayout.openDrawer(GravityCompat.START);
    }

    public void closeDrawer() {
        open = false;
        drawerLayout.closeDrawer(GravityCompat.START);
    }

    public void drawerToggle() {
        if (drawerLayout.isDrawerOpen(GravityCompat.START)) {
            closeDrawer();
        }
        else {
            openDrawer();
        }
    }

    public void setupDrawer() {
        if(!Settings.SHOW_BOTTOM_MENU) {
            // hide bottom menu
            BottomNavigationView bottom_navigation = activity.findViewById(R.id.bottom_navigation);
            bottom_navigation.setVisibility(View.GONE);
        }

        drawerLayout = activity.findViewById(R.id.drawer_layout);
        titleBar = activity.findViewById(R.id.titleBar);
        menu = activity.findViewById(R.id.menu);
        back = activity.findViewById(R.id.back);
        refresh = activity.findViewById(R.id.refresh);
        title = activity.findViewById(R.id.title);

        titleBar.setBackgroundColor(Color.parseColor(Settings.TITLEBAR_BACKGROUND_COLOR));
        if(Settings.TITLEBAR_TINT_COLOR.equals("white")){
            Utils.changeImageViewColor(activity, menu, R.color.white);
            Utils.changeImageViewColor(activity, back, R.color.white);
            Utils.changeImageViewColor(activity, refresh, R.color.white);
            title.setTextColor(activity.getResources().getColor(R.color.white));
        }
        else{
            Utils.changeImageViewColor(activity, menu, R.color.black);
            Utils.changeImageViewColor(activity, back, R.color.black);
            Utils.changeImageViewColor(activity, refresh, R.color.black);
            title.setTextColor(activity.getResources().getColor(R.color.black));
        }
        menu.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Utils.clickEffect(v);
                drawerToggle();
            }
        });
        back.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Utils.clickEffect(v);
                activity.webviewGoBack();
            }
        });
        refresh.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Utils.clickEffect(v);
                LogUtil.loge("onRefresh");
                activity.loadWebPage();
            }
        });
    }

    public void showBack(){
        back.setVisibility(View.VISIBLE);
    }

    public void hideBack(){
        back.setVisibility(View.GONE);
    }
}
