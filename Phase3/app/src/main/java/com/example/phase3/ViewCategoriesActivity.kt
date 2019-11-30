package com.example.phase3

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.app.Activity
import android.content.Context
import android.content.Intent
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.*
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.toolbox.Volley
import com.android.volley.toolbox.StringRequest
import kotlinx.android.synthetic.main.activity_view_categories.*
import com.google.gson.*
import com.squareup.picasso.Picasso
import android.widget.AdapterView
import androidx.core.content.ContextCompat.startActivity

val url = "http://apt-team7.appspot.com"

class ViewCategoriesActivity : AppCompatActivity() {

    fun bind(categories:JsonArray) {
        Log.d("debug", categories.toString())

        val adapter = ListViewCustomAdapter(this, categories, this)
        val listView = findViewById<ListView>(R.id.lstCategories)
        listView.setAdapter(adapter)
    }
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_view_categories)

        val queue = Volley.newRequestQueue(this)
        // 2. Create the request with the callback
        val stringRequest = StringRequest(Request.Method.GET, url + "/mobile",
            Response.Listener {
                response -> run {
                val parser = JsonParser()
                Log.d("json", response)
                val jsonTree = parser.parse(response)
                val categories = jsonTree.asJsonArray
                bind(categories)
                }
            },
            Response.ErrorListener {
                error -> run {
                    txtHeader.text = "Failed to retrieve data"
                    lstCategories.visibility = View.GONE
                    Log.d("error", error.toString())
                }
            })
        queue.add(stringRequest)
    }
}

class ListViewCustomAdapter(var context: Activity, internal var categories:JsonArray, internal var thisView: ViewCategoriesActivity) :
    BaseAdapter() {
    var inflater: LayoutInflater

    init {

        this.inflater = context.getSystemService(Context.LAYOUT_INFLATER_SERVICE) as LayoutInflater
    }

    override fun getCount(): Int {
        // TODO Auto-generated method stub
        return categories.size()
    }

    override fun getItem(position: Int): Any {
        // TODO Auto-generated method stub
        return categories[position]
    }

    override fun getItemId(position: Int): Long {
        // TODO Auto-generated method stub
        return 0
    }

    class ViewHolder {
        internal var listview_image: ImageView? = null
        internal var listview_item_title: TextView? = null
        internal var listview_item_short_description: TextView? = null
    }

    override fun getView(position: Int, view: View?, parent: ViewGroup): View {

        var convertView = view
        // TODO Auto-generated method stub

        val holder: ViewHolder
        if (convertView == null) {
            holder = ViewHolder()
            convertView = inflater.inflate(R.layout.listview_activity, null)

            holder.listview_image = convertView!!.findViewById(R.id.listview_image) as ImageView
            holder.listview_item_title = convertView.findViewById(R.id.listview_item_title) as TextView
            holder.listview_item_short_description =
                convertView.findViewById(R.id.listview_item_short_description) as TextView

            convertView.tag = holder
        } else
            holder = convertView.tag as ViewHolder

        val item = categories.get(position).getAsJsonObject()
        holder.listview_item_title!!.setText(item.get("catName").getAsString())
        holder.listview_item_short_description!!.setText(item.get("catDescription").getAsString())
        val imgUrl = url + "/images/" + item.get("imageId").getAsString()
        Picasso.get().load(imgUrl).into(holder.listview_image)
        Log.d("image","Loaded " + imgUrl + " into " + holder.listview_image!!.id.toString())

        convertView.setOnClickListener(object : View.OnClickListener {
            override fun onClick(v: View) {
                Log.d("position", position.toString())
                val clicked = categories.get(position).getAsJsonObject()
                var catId = clicked.get("cat_id").getAsString()

                val viewCatIntent = Intent(thisView, CategoryReportActivity::class.java)
                viewCatIntent.putExtra("cat_id", catId)
                thisView.startActivity(viewCatIntent)
                Log.d("debug", "Loaded new view to show reports in category " + catId)
            }
        })
        return convertView
    }
}