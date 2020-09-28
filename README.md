# slab_method
Slab method for point location in planar straight-line graph (PSLG)

# Application

## Input

A JSON file that contains PSLG represented by a doubly connected edge list (DCEL) and points that need be located.
All numbers must be integers, and the index of outer face is -1.

Example:
```json
{
  "pslg": {
    "vertexes": [
      {
        "x": 0,
        "y": 0
      },
      {
        "x": 5,
        "y": 5
      },
      {
        "x": 10,
        "y": 0
      },
      {
        "x": 12,
        "y": 8
      }
    ],
    "edges": [
      {
        "v1": 0,
        "v2": 1,
        "f1": -1,
        "f2": 0,
        "p1": 3,
        "p2": 2
      },
      {
        "v1": 3,
        "v2": 1,
        "f1": 1,
        "f2": -1,
        "p1": 4,
        "p2": 0
      },
      {
        "v1": 1,
        "v2": 2,
        "f1": 1,
        "f2": 0,
        "p1": 1,
        "p2": 3
      },
      {
        "v1": 2,
        "v2": 0,
        "f1": -1,
        "f2": 0,
        "p1": 4,
        "p2": 0
      },
      {
        "v1": 3,
        "v2": 2,
        "f1": -1,
        "f2": 1,
        "p1": 1,
        "p2": 2
      }
    ]
  },
  "points": [
    {
      "x": 4,
      "y": 3
    },
    {
      "x": 8,
      "y": 2
    },
    {
      "x": 10,
      "y": 5
    },
    {
      "x": 5,
      "y": 5
    },
    {
      "x": 11,
      "y": 4
    },
    {
      "x": 4,
      "y": -1
    }
  ]
}
```

## Output

1. If successful, a JSON file that contains indices of faces in which points were located:

   ```json
   {
     "faces": [
       0,
       1,
       1,
       1,
       1,
       -1
     ]
   }
   ```

2. If a fault, a JSON file that contains an error. For example:

   ```json
   {
     "error": "Incorrect graph: pointer points on the same edge"
   }
   ```

## Running

```bash
python main.py -i in.json -o out.json
```
