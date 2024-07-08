package com.app.sravz333;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.Dialog;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.view.Gravity;
import android.view.MenuItem;
import android.view.View;
import android.view.Window;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.PopupMenu;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;

import java.util.ArrayList;

/*import com.abdeveloper.library.MultiSelectDialog;
import com.abdeveloper.library.MultiSelectModel;
import android.support.v7.app.AppCompatActivity;*/

public class PopupUtil {
    public interface AlertPopup {
        void positive(DialogInterface dialog);
        void negative(DialogInterface dialog);
    }

    // buttons sequence: positive, negative
    public static void showAlertPopup(Activity activity, String title, String message, String [] buttons, final AlertPopup alert){
        AlertDialog.Builder builder = new AlertDialog.Builder(activity);
        builder.setTitle(title);
        builder.setMessage(message);
        for (int i = 0; i < buttons.length; i++) {
            if(i==0){
                builder.setPositiveButton(buttons[i], new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        alert.positive(dialog);
                    }
                });
            }
            else if(i==1){
                builder.setNegativeButton(buttons[i], new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        alert.negative(dialog);
                    }
                });
            }
        }
        builder.show();
    }

    public interface SingleChoicePopup{
        void selection(int which);
    }

    private static int index;
    public static void showSingleChoicePopup(Activity activity, String title, String [] options, @NonNull String selected, final SingleChoicePopup singleChoicePopup) {
        AlertDialog.Builder builder = new AlertDialog.Builder(activity);
        builder.setTitle(title);
        index = -1;
        for (int i = 0; i < options.length; i++) {
            if(selected.equals(options[i])){
                index = i;
                break;
            }
        }
        builder.setSingleChoiceItems(options, index, null);
        builder.setPositiveButton("Done", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {
                if(index == -1)
                    index = 0;
                singleChoicePopup.selection(index);
            }
        });
        AlertDialog dialog = builder.create();
        dialog.show();
        final ListView listView = dialog.getListView();
        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int position, long l) {
                boolean isChecked = listView.isItemChecked(position);
                if(isChecked) {
                    index = position;
                }
            }
        });
    }

    public interface MultiChoicePopup{
        void selection(String selectedString);
    }

    public static void showMultiChoicePopup(final Activity activity, final String title, final String [] options, @NonNull final String selectedString, final MultiChoicePopup multiChoicePopup) {
        AlertDialog.Builder builder = new AlertDialog.Builder(activity);
        final boolean [] selectedBoolean = new boolean[options.length];
        String [] arr = selectedString.split(",");
        for (int i = 0; i < options.length; i++) {
            selectedBoolean[i] = false;
            for (String s : arr) {
                if(options[i].equals(s)){
                    selectedBoolean[i] = true;
                }
            }
        }
        // check select all
        if(arr.length+1 == options.length){
            selectedBoolean[0] = true;
        }
        builder.setTitle(title)
                .setMultiChoiceItems(options, selectedBoolean, null)
                .setPositiveButton("Done", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int id) {
                        StringBuilder sb = new StringBuilder();
                        for (int j = 1; j < options.length; j++) {
                            if(selectedBoolean[j]){
                                sb.append(options[j]);
                                sb.append(",");
                            }
                        }
                        String selectedString = sb.toString();
                        if(selectedString.endsWith(",")){
                            selectedString = selectedString.substring(0, selectedString.length()-1);
                        }
                        multiChoicePopup.selection(selectedString);
                    }
                });
        AlertDialog dialog = builder.create();
        dialog.show();
        final ListView listView = dialog.getListView();
        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            boolean selectAll = true;
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int position, long l) {
                boolean isChecked = listView.isItemChecked(position);
                selectedBoolean[position] = isChecked;
                if (position == 0) {
                    if(selectAll) {
                        for (int i = 1; i < options.length; i++) { // we start with first element after "Select all" choice
                            if (isChecked && !listView.isItemChecked(i)
                                    || !isChecked && listView.isItemChecked(i)) {
                                listView.performItemClick(listView, i, 0);
                            }
                        }
                    }
                }
                else {
                    if (!isChecked && listView.isItemChecked(0)) {
                        // if other item is unselected while "Select all" is selected, unselect "Select all"
                        // false, performItemClick, true is a must in order for this code to work
                        selectAll = false;
                        listView.performItemClick(listView, 0, 0);
                        selectAll = true;
                    }
                }
            }
        });
    }

    public static Dialog showCustomPopup(Activity activity, int layout) {
        Dialog dialog = new Dialog(activity);
        dialog.requestWindowFeature(Window.FEATURE_NO_TITLE);
        dialog.setCancelable(true);
        dialog.setContentView(layout);
        dialog.show();
        return dialog;
    }

    public interface MenuPopup{
        void selection(String title);
    }
    public static void showMenuPopup(Activity activity, View view, ArrayList<String> options, final MenuPopup menuPopup){
        PopupMenu popup = new PopupMenu(activity, view);
        for (String option : options) {
            popup.getMenu().add(option);
        }
        popup.show();
        popup.setOnMenuItemClickListener(new PopupMenu.OnMenuItemClickListener() {
            @Override
            public boolean onMenuItemClick(MenuItem menuItem) {
                menuPopup.selection((String) menuItem.getTitle());
                return true;
            }
        });
    }

    //-------------------------------------Searchable Multi Select Popup---------------------------------------

    /*
    maven {
        url 'https://jitpack.io'
    }
    implementation 'com.github.abumoallim:Android-Multi-Select-Dialog:v1.9'

    public interface SearchablePopup{
        void selection(String selectedString);
    }

    public static void showSearchablePopup(AppCompatActivity activity, String title, ArrayList<MultiSelectModel> list, String selectedString, final SearchablePopup searchablePopup){
        ArrayList<Integer> selectedList = new ArrayList<>();
        String [] arr = selectedString.split(", ");
        for (int i = 0; i < list.size(); i++) {
            for (String s : arr) {
                if (list.get(i).getName().replace(" ","").equals(s.replace(" ",""))) {
                    selectedList.add(list.get(i).getId());
                }
            }
        }
        MultiSelectDialog multiSelectDialog = new MultiSelectDialog()
            .title(title)
            .titleSize(25)
            .positiveText("Done")
            .negativeText("Cancel")
            .setMinSelectionLimit(1) //you can set minimum checkbox selection limit (Optional)
            .setMaxSelectionLimit(list.size()) //you can set maximum checkbox selection limit (Optional)
            .preSelectIDsList(selectedList) //List of ids that you need to be selected
            .multiSelectList(list) // the multi select model list with ids and name
            .onSubmit(new MultiSelectDialog.SubmitCallbackListener() {
                @Override
                public void onSelected(ArrayList<Integer> selectedIds, ArrayList<String> selectedNames, String dataString) {
                    searchablePopup.selection(dataString);
                }
                @Override
                public void onCancel() {
                }
            });
        multiSelectDialog.show(activity.getSupportFragmentManager(), "multiSelectDialog");
    }
    */

    private static ProgressDialog progressDialog;
    public static void showProgress(Activity activity, String loadingMsg, boolean cancelAble){
        progressDialog = new ProgressDialog(activity);
        progressDialog.setCancelable(cancelAble);
        progressDialog.setMessage(loadingMsg);
        progressDialog.show();
    }

    public static void hideProgress(){
        if(progressDialog != null) {
            if (progressDialog.isShowing()) {
                progressDialog.hide();
                progressDialog = null;
            }
        }
    }

    public static final String TOP = "top";
    public static final String BOTTOM = "bottom";

    public static Toast showToastShort(Activity mAct, String text, int bgColor, int txtColor, String position) {
        final Toast toast = Toast.makeText(mAct, text, Toast.LENGTH_SHORT);
        if(position.equals(TOP)) {
            toast.setGravity(Gravity.FILL_HORIZONTAL | Gravity.TOP, 0, 0);
        }
        else {
            toast.setGravity(Gravity.FILL_HORIZONTAL | Gravity.BOTTOM, 0, 0);
        }
        View tView = toast.getView();
        tView.setBackgroundColor(bgColor);
        TextView mText = tView.findViewById(android.R.id.message);
        mText.setTextColor(txtColor);
        mText.setPadding(20, 0,20,0);
        mText.setShadowLayer(0, 0, 0, 0);
        tView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                toast.cancel();
            }
        });
        tView.invalidate();
        toast.show();
        return toast;
    }

    public static Toast showToastLong(Activity mAct, String text, int bgColor, int txtColor, String position) {
        final Toast toast = Toast.makeText(mAct, text, Toast.LENGTH_LONG);
        if(position.equals(TOP)) {
            toast.setGravity(Gravity.FILL_HORIZONTAL | Gravity.TOP, 0, 0);
        }
        else {
            toast.setGravity(Gravity.FILL_HORIZONTAL | Gravity.BOTTOM, 0, 0);
        }
        View tView = toast.getView();
        tView.setBackgroundColor(bgColor);
        TextView mText = tView.findViewById(android.R.id.message);
        mText.setTextColor(txtColor);
        mText.setPadding(20, 0,20,0);
        mText.setShadowLayer(0, 0, 0, 0);
        tView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                toast.cancel();
            }
        });
        tView.invalidate();
        toast.show();
        return toast;
    }
}
