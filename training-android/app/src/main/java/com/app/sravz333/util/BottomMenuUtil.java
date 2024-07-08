package com.app.sravz333.util;

import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.drawerlayout.widget.DrawerLayout;

import com.app.sravz333.Home;
import com.app.sravz333.R;
import com.app.sravz333.Settings;
import com.google.android.material.bottomnavigation.BottomNavigationView;

public class BottomMenuUtil {

    public static void setBottomMenu(final Home activity){
        if(!Settings.SHOW_DRAWER) {
            // hide title bar
            ViewGroup titleBar = activity.findViewById(R.id.titleBar);
            titleBar.setVisibility(View.GONE);
            // disable drawer gesture
            DrawerLayout drawerLayout = activity.findViewById(R.id.drawer_layout);
            drawerLayout.setDrawerLockMode(DrawerLayout.LOCK_MODE_LOCKED_CLOSED);
        }

        BottomNavigationView bottom_navigation = activity.findViewById(R.id.bottom_navigation);
        bottom_navigation.setItemBackgroundResource(R.color.bottomNavigationBackgroundColor);

        Menu menu = bottom_navigation.getMenu();
        menu.clear();
        for (int i = 0; i < Settings.BOTTOM_MENU_TITLES.length; i++) {
            String title = Settings.BOTTOM_MENU_TITLES[i];
            MenuItem item = menu.add(
                    Menu.NONE, // groupId
                    i+1, // itemId
                    i+1, // order
                    title // title
            );
            if(Settings.SHOW_BOTTOM_MENU_ICONS) {
                item.setIcon(Settings.BOTTOM_MENU_ICONS[i]);
            }
        }
        bottom_navigation.setOnNavigationItemSelectedListener(new BottomNavigationView.OnNavigationItemSelectedListener() {
            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem item) {
                LogUtil.loge("onNavigationItemSelected: "+item.getItemId());
                activity.loadWebPageFromBottomMenu(Settings.BOTTOM_MENU_LINKS[item.getItemId()-1]);
                return true;
            }
        });
    }
}
