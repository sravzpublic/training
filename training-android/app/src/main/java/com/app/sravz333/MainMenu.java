package com.app.sravz333;

import android.graphics.Color;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ListView;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

public class MainMenu extends Fragment {
    ViewGroup main;
    ListView listView;
    MainMenuAdapter mainMenuAdapter;

    public static MainMenu newInstance() {
        MainMenu fragment = new MainMenu();
        Bundle args = new Bundle();
        //args.putString("type", type);
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.main_menu, container, false);
        main = view.findViewById(R.id.main);
        listView = view.findViewById(R.id.listView);
        return view;
    }

    @Override
    public void onActivityCreated(@Nullable Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);

        if(!Settings.SHOW_DRAWER){
            return;
        }

        main.setBackgroundColor(Color.parseColor(Settings.DRAWER_BACKGROUND_COLOR));
        mainMenuAdapter = new MainMenuAdapter(getActivity());
        listView.setAdapter(mainMenuAdapter);
        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                Home home = (Home)getActivity();
                if(home != null){
                    home.loadWebPageFromDrawer(Settings.DRAWER_LINKS[position]);
                }
            }
        });
    }
}
