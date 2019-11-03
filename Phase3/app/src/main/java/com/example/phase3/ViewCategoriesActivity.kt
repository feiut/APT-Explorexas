package com.example.phase3

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.ListView
import android.widget.SimpleAdapter
import android.R.drawable.presence_online
import android.R.drawable.presence_offline
import android.util.Log
import android.view.View
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.toolbox.Volley
import com.android.volley.toolbox.StringRequest
import kotlinx.android.synthetic.main.activity_view_categories.*

class ViewCategoriesActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_view_categories)

        val queue = Volley.newRequestQueue(this)
        // 2. Create the request with the callback
        val url = "http://explore-texas-web.appspot.com/"
        val stringRequest = StringRequest(Request.Method.GET, url,
            Response.Listener {
                    response -> Log.d("soap_request", response)
            },
            Response.ErrorListener {
                error -> run {
                    txtHeader.text = "Failed to retrieve data"
                    lstCategories.visibility = View.GONE
                    Log.d("error", error.toString())
                }
            })
        queue.add(stringRequest)

        val listviewTitle = arrayOf(
            "ListView Title 1",
            "ListView Title 2",
            "ListView Title 3",
            "ListView Title 4",
            "ListView Title 5",
            "ListView Title 6",
            "ListView Title 7",
            "ListView Title 8"
        )


        val listviewImage = intArrayOf(
            presence_online,
            presence_offline,
            presence_online,
            presence_online,
            presence_offline,
            presence_online,
            presence_online,
            presence_offline
        )

        val listviewShortDescription = arrayOf(
            "Android ListView Short Description",
            "Android ListView Short Description",
            "Android ListView Short Description",
            "Android ListView Short Description",
            "Android ListView Short Description",
            "Android ListView Short Description",
            "Android ListView Short Description",
            "Android ListView Short Description"
        )

        val aList = ArrayList<HashMap<String, String>>()

        for (i in 0..7) {
            val hm = HashMap<String, String>()
            hm["listview_title"] = listviewTitle[i]
            hm["listview_discription"] = listviewShortDescription[i]
            hm["listview_image"] = Integer.toString(listviewImage[i])
            aList.add(hm)
        }

        val from = arrayOf("listview_image", "listview_title", "listview_discription")
        val to = intArrayOf(
            R.id.listview_image,
            R.id.listview_item_title,
            R.id.listview_item_short_description
        )

        val simpleAdapter = SimpleAdapter(baseContext, aList, R.layout.listview_activity, from, to)
        val androidListView = findViewById(R.id.lstCategories) as ListView
        androidListView.setAdapter(simpleAdapter)
    }
}
