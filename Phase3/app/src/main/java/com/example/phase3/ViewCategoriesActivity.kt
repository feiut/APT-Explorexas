package com.example.phase3

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.ListView
import android.widget.SimpleAdapter
import android.R.drawable.presence_online
import android.R.drawable.presence_offline
import javax.swing.UIManager.put
import androidx.core.app.ComponentActivity.ExtraData
import androidx.core.content.ContextCompat.getSystemService
import android.icu.lang.UCharacter.GraphemeClusterBreak.T
import android.util.Log
import android.volley.Request
import android.volley.RequestQueue
import android.volley.toolbox.Volley


class ViewCategoriesActivity : AppCompatActivity() {

    fun getCategories() {

    }

    fun HttpPOSTRequestWithParam() {
        val queue = Volley.newRequestQueue(this)
        val url = "http://www.yourwebstite.com/login.asp"
        val postRequest = object : StringRequest(Request.Method.POST, url,
            object : Response.Listener<String>() {
                fun onResponse(response: String) {
                    Log.d("Response", response)
                }
            },
            object : Response.ErrorListener() {
                fun onErrorResponse(error: VolleyError) {
                    Log.d("ERROR", "error => " + error.toString())
                }
            }
        ) {

            protected// volley will escape this for you
            val params: Map<String, String>
                get() {
                    val params = HashMap<String, String>()
                    params["grant_type"] = "password"

                    params["username"] = "tester"
                    params["password"] = "Pass@123"

                    return params
                }
        }
        queue.add(postRequest)
    }
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_view_categories)

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
        val androidListView = findViewById(R.id.list_view) as ListView
        androidListView.setAdapter(simpleAdapter)
    }
}
